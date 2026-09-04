#!/usr/bin/env python3
import os
import re
import shutil
import subprocess
import sys
import tempfile

GREEN = "\033[0;32m"
YELLOW = "\033[1;33m"
RED = "\033[0;31m"
CYAN = "\033[0;36m"
NC = "\033[0m"

USAGE = f"""{CYAN}gits{NC} - 智能 GitHub 内容下载与同步工具

{GREEN}用法:{NC}
  gits <github-url> [目标路径]
  gits push [to <仓库地址>] ["备注"] [-f]
  gits pull [路径]

{GREEN}下载模式:{NC}
  仓库:   https://github.com/owner/repo
  文件夹: https://github.com/owner/repo/tree/branch/path
  文件:   https://github.com/owner/repo/blob/branch/path/file

{GREEN}同步模式 (Push):{NC}
  gits push                  # 快速同步 (默认备注: 日常同步更新)
  gits push "修改了xxx"      # 带备注同步
  gits push to <url>         # 首次关联仓库并同步
  gits push to <url> "备注"  # 首次关联并带备注同步
  gits push "备注" -f        # 强制推送 (覆盖远程)

{GREEN}拉取模式 (Pull):{NC}
  gits pull                  # 拉取当前目录仓库
  gits pull <路径>           # 拉取指定路径仓库

{GREEN}特性:{NC}
  ✓ 自动识别仓库/文件夹/文件
  ✓ 智能同步：自动 init, add, commit, push
  ✓ 分支自动对齐：智能处理 master/main 差异
  ✓ 不指定路径默认下载到当前目录
"""


def info(msg):
    print(f"{GREEN}[+]{NC} {msg}")


def warn(msg):
    print(f"{YELLOW}[!]{NC} {msg}")


def error(msg):
    print(f"{RED}[-]{NC} {msg}")
    sys.exit(1)


def step(msg):
    print(f"{CYAN}[*]{NC} {msg}")


def run(cmd, **kwargs):
    kwargs.setdefault("capture_output", False)
    return subprocess.run(cmd, **kwargs)


def run_quiet(cmd):
    return subprocess.run(cmd, capture_output=True, text=True)


def is_git_repo(path="."):
    r = run_quiet(["git", "-C", path, "rev-parse", "--is-inside-work-tree"])
    return r.returncode == 0


def has_origin():
    r = run_quiet(["git", "remote", "get-url", "origin"])
    return r.returncode == 0


def current_branch():
    r = run_quiet(["git", "branch", "--show-current"])
    branch = r.stdout.strip()
    if not branch:
        run_quiet(["git", "checkout", "-b", "main"])
        branch = "main"
    return branch


def git_pull(path):
    r = run(["git", "-C", path, "pull"])
    if r.returncode == 0:
        info("拉取完成! ✨")


def git_push(force):
    branch = current_branch()
    args = ["git", "push", "-u", "origin"]
    if force:
        warn("正在强制推送 (-f)，将覆盖远程版本!")
        args.append("-f")
    args.append(f"{branch}:main")
    r = run(args)
    if r.returncode != 0:
        error("推送失败")
    info("推送成功!")


def parse_url(url):
    url = url.rstrip("/")
    if url.endswith(".git"):
        url = url[:-4]
    m = re.match(r"^https://github\.com/([^/]+)/([^/]+)/tree/([^/]+)/(.+)$", url)
    if m:
        return "folder", m.group(1), m.group(2), m.group(3), m.group(4)
    m = re.match(r"^https://github\.com/([^/]+)/([^/]+)/blob/([^/]+)/(.+)$", url)
    if m:
        return "file", m.group(1), m.group(2), m.group(3), m.group(4)
    m = re.match(r"^https://github\.com/([^/]+)/([^/]+)$", url)
    if m:
        return "repo", m.group(1), m.group(2), None, None
    error("无法识别的 GitHub 链接格式")
    return None, None, None, None, None


def resolve_target(path, item_name):
    if path.endswith("/"):
        os.makedirs(path, exist_ok=True)
        return os.path.join(path, item_name)
    if os.path.isdir(path):
        return os.path.join(path, item_name)
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    return path


def handle_conflict(final_path):
    if os.path.lexists(final_path):
        warn(f"目标已存在: {final_path}")
        answer = input("是否覆盖? [y/N] ").strip()
        if not re.match(r"^[Yy]$", answer):
            info("已取消")
            sys.exit(0)
        if os.path.isdir(final_path) and not os.path.islink(final_path):
            shutil.rmtree(final_path)
        else:
            os.remove(final_path)


def download_repo(repo_url, final_path):
    step("正在克隆整个仓库 (浅克隆)...")
    r = run(["git", "clone", "--depth=1", repo_url, final_path])
    if r.returncode != 0:
        error("克隆失败")


def download_folder(repo_url, branch, path_in_repo, final_path):
    tmp_dir = tempfile.mkdtemp()
    try:
        step("正在获取仓库元数据...")
        r = run_quiet([
            "git", "clone", "--filter=blob:none", "--no-checkout",
            "--single-branch", "--branch", branch, repo_url, tmp_dir,
        ])
        if r.returncode != 0:
            error("克隆仓库失败")

        step(f"正在设置稀疏检出: {path_in_repo}")
        run(["git", "-C", tmp_dir, "sparse-checkout", "init", "--cone"])
        r = run(["git", "-C", tmp_dir, "sparse-checkout", "set", path_in_repo])
        if r.returncode != 0:
            error("稀疏检出失败")
        run(["git", "-C", tmp_dir, "checkout", branch])

        step("正在提取文件夹...")
        os.makedirs(os.path.dirname(final_path) or ".", exist_ok=True)
        shutil.copytree(os.path.join(tmp_dir, path_in_repo), final_path)
    finally:
        shutil.rmtree(tmp_dir, ignore_errors=True)


def download_file(owner, repo, branch, path_in_repo, final_path):
    raw_url = f"https://raw.githubusercontent.com/{owner}/{repo}/{branch}/{path_in_repo}"
    step("正在下载文件...")
    r = run(["curl", "-L", "--progress-bar", "-o", final_path, raw_url])
    if r.returncode != 0:
        error("文件下载失败")


def main():
    args = sys.argv[1:]

    if not args or args[0] in ("-h", "--help"):
        print(USAGE)
        sys.exit(0)

    # ================= Pull 模式 =================
    if args[0] == "pull":
        target_dir = os.path.expandvars(os.path.expanduser(args[1] if len(args) > 1 else "."))
        if not os.path.isdir(target_dir):
            error(f"目录不存在: {target_dir}")
        if not is_git_repo(target_dir):
            warn(f"未检测到 Git 仓库: {target_dir}")
            sys.exit(0)
        step("正在从远程仓库拉取更新...")
        info(f"当前目录: {CYAN}{os.path.abspath(target_dir)}{NC}")
        git_pull(target_dir)
        sys.exit(0)

    # ================= Push 模式 =================
    force_push = False
    if args[-1] == "-f":
        force_push = True
        args = args[:-1]

    if args[0] == "push":
        args = args[1:]
        remote_url = ""
        msg = "日常同步更新"

        if args and args[0] == "to":
            if len(args) < 2:
                error("请提供仓库地址，例如: gits push to https://github.com/xxx/xxx")
            remote_url = args[1]
            msg = args[2] if len(args) > 2 else "日常同步更新"
        elif args:
            msg = args[0]

        # 1. 检查/初始化仓库
        if not is_git_repo():
            step("未检测到 Git 仓库，正在初始化...")
            r = run_quiet(["git", "init", "-b", "main"])
            if r.returncode != 0:
                run(["git", "init"])
            info("仓库已初始化")

        # 2. 处理远程仓库
        has_origin_flag = has_origin()
        if remote_url:
            if has_origin_flag:
                step("更新远程仓库地址...")
                run(["git", "remote", "set-url", "origin", remote_url])
            else:
                step("关联远程仓库...")
                run(["git", "remote", "add", "origin", remote_url])
            info(f"远程仓库已关联: {remote_url}")
        elif not has_origin_flag:
            warn("未关联远程仓库")
            input_url = input("请输入 GitHub 仓库地址 (回车取消): ").strip()
            if not input_url:
                error("已取消")
            run(["git", "remote", "add", "origin", input_url])
            info(f"远程仓库已关联: {input_url}")

        # 3. 当前分支
        branch = current_branch()

        # 4. Add & Commit
        step("正在暂存文件...")
        run(["git", "add", "."])
        diff = run_quiet(["git", "diff-index", "--quiet", "HEAD", "--"])
        if diff.returncode == 0:
            warn("没有检测到文件变更，跳过提交")
        else:
            step("正在提交更改...")
            run(["git", "commit", "-m", msg])

        # 5. Push
        step("正在推送到 GitHub (远程分支: main)...")
        git_push(force_push)

        print()
        info(f"同步完成! 分支: {branch} ✨")
        sys.exit(0)

    # ================= 下载模式 =================
    url = args[0]
    target_path = os.path.expandvars(os.path.expanduser(args[1] if len(args) > 1 else "."))

    mode, owner, repo, branch, path_in_repo = parse_url(url)
    item_name = os.path.basename(path_in_repo) if path_in_repo else repo
    repo_url = f"https://github.com/{owner}/{repo}.git"

    info(f"模式: {CYAN}{mode}{NC} | 仓库: {CYAN}{owner}/{repo}{NC}")

    final_path = resolve_target(target_path, item_name)
    handle_conflict(final_path)

    if mode == "repo":
        download_repo(repo_url, final_path)
    elif mode == "folder":
        download_folder(repo_url, branch, path_in_repo, final_path)
    else:
        download_file(owner, repo, branch, path_in_repo, final_path)

    print()
    info(f"完成! 已保存到: {CYAN}{final_path}{NC} ✨")


if __name__ == "__main__":
    main()