# 🆘 重要数据误删急救指南

别慌！数据恢复是有很大希望的，关键是**立刻按顺序做以下几件事**：

---

## ⚡ 第一步：立即停止写入（最关键！）

**千万不要**继续往被删文件所在的磁盘分区写任何新数据！
- 关闭所有可能写入该分区的软件
- 避免下载、安装、保存新文件
- 因为删除只是删除了"目录引用"，数据还在磁盘上，新写入会覆盖它

---

## 🔍 第二步：检查是否有备份

| 备份渠道 | 检查方法 |
|---------|---------|
| macOS Time Machine | 进入 Time Machine，浏览历史版本，直接恢复 |
| Windows 文件历史 | 右键文件夹 → 属性 → 以前的版本 |
| 云盘（iCloud / Google Drive / OneDrive） | 网页端查看"回收站"或"版本历史" |
| 自己做过备份 | 检查外置硬盘、NAS 或网盘 |
| 代码有 Git 管理 | `git fsck --lost-found` 或 `git reflog` |

---

## 🛠️ 第三步：使用数据恢复工具

### macOS
```
# 查看是否有 APFS 快照可用
tmutil listlocalsnapshots /
```

### Linux
```bash
# 先卸载该分区（重要！）
sudo umount /dev/sdXN

# 使用 extundelete（EXT 文件系统）
sudo apt install extundelete
sudo extundelete /dev/sdXN --restore-all

# 或使用 photorec（通用工具，更强大）
sudo apt install testdisk
sudo photorec
```

### Windows
- **Recuva**（免费，适合普通文件）
- **PhotoRec**（免费，支持几乎所有文件系统）
- **Disk Drill**（有免费版本）
- **R-Studio**（专业级，付费）

---

## 📁 第四步：按文件类型处理

### 文档 / 代码
- 检查编辑器的"最近打开"列表
- 检查 `~/.Trash`（macOS）或 `$RECYCLE.BIN`（Windows）
- Git 用户：`git reflog` 可找回已提交但丢失的提交

### 照片 / 视频
- SD 卡 / U盘：立刻拔出不再使用
- 相机机身内删除：停止拍摄，使用 PhotoRec 恢复

### 数据库 / 重要文件
- 如果是 MySQL / PostgreSQL：立即停库，查看 binlog
- 虚拟机快照：从快照恢复

---

## 💡 预防措施（以后不再慌）

1. **开启 Time Machine / Windows 文件历史**（系统自动备份）
2. **重要文件同步到云盘**（iCloud / Google Drive / OneDrive）
3. **代码用 Git 管理**（`git commit` 是免费的保险）
4. **定期手动备份到外置硬盘**
5. **敏感数据使用版本控制工具**（如 Dropbox 的历史版本）
6. **分区操作前提前备份**

---

## 🆘 还是搞不定？

- 停止自己折腾，立刻停止写保护
- 找专业数据恢复公司（本地线下店）
- 用 Live CD/USB 启动，完全不碰原系统盘

**记住：越早停止写入，恢复成功的概率越高！** 💪
