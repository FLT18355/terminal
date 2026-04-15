#!/data/data/com.termux/files/usr/bin/node

const fs = require('fs');
const path = require('path');
const { exec } = require('child_process');
const readline = require('readline');

class MusicPlayer {
    constructor() {
        this.file = null;
        this.lyrics = [];
        this.process = null;
        this.playing = false;
        this.startTime = 0;
        this.pauseTime = 0;
        this.lyricFile = null;
        this.running = true;
        this.refreshInterval = null;
        this.allLrcFiles = [];
        this.loopMode = false;
        this.songEnded = false;
        
        this.rl = readline.createInterface({
            input: process.stdin,
            output: process.stdout
        });
    }

    colors = {
        reset: '\x1b[0m',
        red: '\x1b[31m',
        green: '\x1b[32m',
        yellow: '\x1b[33m',
        blue: '\x1b[34m',
        magenta: '\x1b[35m',
        cyan: '\x1b[36m',
        white: '\x1b[37m',
        gray: '\x1b[90m',
        bold: '\x1b[1m',
        dim: '\x1b[2m'
    };

    async chooseLyricsFile(musicFile) {
        console.log(`\n${this.colors.cyan}📋 选择歌词文件:${this.colors.reset}`);
        
        const dir = path.dirname(musicFile);
        
        try {
            this.allLrcFiles = fs.readdirSync(dir)
                .filter(f => f.endsWith('.lrc'))
                .map(f => path.join(dir, f));
            
            if (this.allLrcFiles.length === 0) {
                console.log(`   ${this.colors.red}❌ 没有找到 .lrc 文件${this.colors.reset}`);
                return null;
            }
            
            console.log(`   ${this.colors.green}找到 ${this.allLrcFiles.length} 个歌词文件:${this.colors.reset}\n`);
            this.allLrcFiles.forEach((f, i) => {
                const stats = fs.statSync(f);
                const size = (stats.size / 1024).toFixed(1);
                console.log(`   ${this.colors.yellow}${i+1}.${this.colors.reset} ${this.colors.cyan}${path.basename(f)}${this.colors.reset} ${this.colors.gray}(${size} KB)${this.colors.reset}`);
            });
            
            console.log(`\n   ${this.colors.yellow}0.${this.colors.reset} ${this.colors.gray}不使用歌词${this.colors.reset}`);
            
            const answer = await this.question(`\n${this.colors.green}选择编号: ${this.colors.reset}`);
            const num = parseInt(answer);
            
            if (num === 0) return null;
            if (num > 0 && num <= this.allLrcFiles.length) {
                console.log(`   ${this.colors.green}✅ 已选择: ${this.colors.cyan}${path.basename(this.allLrcFiles[num-1])}${this.colors.reset}`);
                return this.allLrcFiles[num-1];
            }
            return null;
        } catch (err) {
            console.log(`   ${this.colors.red}❌ 读取失败: ${err.message}${this.colors.reset}`);
            return null;
        }
    }

    loadLyrics(lrcPath) {
        const lyrics = [];
        try {
            const content = fs.readFileSync(lrcPath, 'utf-8');
            const lines = content.split('\n');
            
            for (let line of lines) {
                const matches = [...line.matchAll(/\[(\d+):(\d+\.?\d*)\]/g)];
                if (matches.length > 0) {
                    let text = line.replace(/\[\d+:\d+\.?\d*\]/g, '').trim();
                    if (text) {
                        for (let match of matches) {
                            const minutes = parseInt(match[1]);
                            const seconds = parseFloat(match[2]);
                            const time = minutes * 60 + seconds;
                            lyrics.push({ time, text });
                        }
                    }
                }
            }
            
            lyrics.sort((a, b) => a.time - b.time);
            return lyrics;
        } catch {
            return [];
        }
    }

    async play(filePath) {
        console.log(`\n${this.colors.green}▶️ 播放: ${this.colors.cyan}${path.basename(filePath)}${this.colors.reset}`);
        this.file = filePath;
        
        this.lyricFile = await this.chooseLyricsFile(filePath);
        this.lyrics = this.lyricFile ? this.loadLyrics(this.lyricFile) : [];
        
        this.startPlayback();
        return true;
    }

    startPlayback() {
        if (this.process) {
            exec(`kill -TERM ${this.process.pid}`);
        }
        
        this.process = exec(`play -q "${this.file}"`);
        this.playing = true;
        this.startTime = Date.now() / 1000;
        this.songEnded = false;
        
        // 监听进程结束
        this.process.on('exit', (code) => {
            if (this.loopMode && this.playing && this.file) {
                console.log(`\n${this.colors.green}🔄 循环播放: ${path.basename(this.file)}${this.colors.reset}`);
                this.startPlayback(); // 重新播放
            } else {
                this.songEnded = true;
                this.playing = false;
            }
        });
        
        this.startAutoRefresh();
    }

    pause() {
        if (!this.process) return;
        
        if (this.playing) {
            exec(`kill -STOP ${this.process.pid}`);
            this.playing = false;
            this.pauseTime = Date.now() / 1000;
        } else {
            exec(`kill -CONT ${this.process.pid}`);
            this.playing = true;
            const pauseDuration = Date.now() / 1000 - this.pauseTime;
            this.startTime += pauseDuration;
        }
        this.displayPlayer();
    }

    stop() {
        if (this.process) {
            exec(`kill -TERM ${this.process.pid}`);
            this.process = null;
        }
        this.playing = false;
        this.file = null;
        this.songEnded = false;
        
        if (this.refreshInterval) {
            clearInterval(this.refreshInterval);
            this.refreshInterval = null;
        }
    }

    toggleLoop() {
        this.loopMode = !this.loopMode;
        const status = this.loopMode ? '开启' : '关闭';
        console.log(`\n${this.colors.cyan}🔄 循环模式: ${this.loopMode ? this.colors.green : this.colors.gray}${status}${this.colors.reset}`);
        this.displayPlayer();
        
        // 如果当前歌曲已经结束但还在循环模式，重新播放
        if (this.loopMode && this.songEnded && this.file) {
            this.startPlayback();
        }
    }

    getLyricsAtTime(elapsed) {
        if (!this.lyrics.length) return { current: null, next: null };
        
        let current = null;
        let next = null;
        
        for (let i = 0; i < this.lyrics.length; i++) {
            if (this.lyrics[i].time <= elapsed) {
                current = this.lyrics[i].text;
            } else {
                next = this.lyrics[i].text;
                break;
            }
        }
        
        return { current, next };
    }

    getProgress() {
        if (!this.playing || !this.lyrics.length) return 0;
        const elapsed = Date.now() / 1000 - this.startTime;
        const total = this.lyrics[this.lyrics.length - 1].time;
        return Math.min(100, elapsed * 100 / total);
    }

    getCurrentTime() {
        if (!this.playing) return 0;
        return Date.now() / 1000 - this.startTime;
    }

    formatTime(seconds) {
        const mins = Math.floor(seconds / 60);
        const secs = Math.floor(seconds % 60);
        return `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
    }

    listMusicFiles() {
        const files = fs.readdirSync('.');
        const audioExts = ['.mp3', '.wav', '.flac', '.m4a', '.ogg', '.aac'];
        return files.filter(f => audioExts.some(ext => f.toLowerCase().endsWith(ext))).sort();
    }

    clearScreen() {
        console.log('\x1b[2J\x1b[H');
    }

    displayPlayer() {
        this.clearScreen();
        
        // 标题
        console.log(`${this.colors.magenta}${this.colors.bold}🎵 歌词播放器${this.colors.reset}`);
        console.log(`${this.colors.gray}────────────────────────────────────────${this.colors.reset}`);
        
        // 当前播放信息
        if (this.file) {
            console.log(`${this.colors.cyan}📀 正在播放:${this.colors.reset} ${this.colors.white}${path.basename(this.file)}${this.colors.reset}`);
            if (this.lyricFile) {
                console.log(`${this.colors.cyan}📝 歌词:${this.colors.reset} ${this.colors.white}${path.basename(this.lyricFile)}${this.colors.reset} ${this.colors.gray}(${this.lyrics.length}行)${this.colors.reset}`);
            }
            
            // 循环模式
            const loopStatus = this.loopMode ? 
                `${this.colors.green}● 开启${this.colors.reset}` : 
                `${this.colors.gray}○ 关闭${this.colors.reset}`;
            console.log(`${this.colors.cyan}🔄 循环:${this.colors.reset} ${loopStatus}`);
            
            console.log(`${this.colors.gray}────────────────────────────────────────${this.colors.reset}`);
            
            // 歌词显示
            if (this.playing && this.lyrics.length) {
                const elapsed = Date.now() / 1000 - this.startTime;
                const { current, next } = this.getLyricsAtTime(elapsed);
                
                if (current) {
                    console.log(`\n${this.colors.yellow}${this.colors.bold}${current}${this.colors.reset}\n`);
                } else {
                    console.log(`\n${this.colors.gray}${this.colors.dim}[ 前奏 ]${this.colors.reset}\n`);
                }
                
                if (next) {
                    console.log(`${this.colors.gray}${this.colors.dim}${next}${this.colors.reset}`);
                }
                
                // 进度条（循环模式下也显示，让用户知道当前进度）
                const progress = this.getProgress();
                const barLen = 30;
                const filled = Math.floor(barLen * progress / 100);
                const bar = '█'.repeat(filled) + '░'.repeat(barLen - filled);
                console.log(`\n${this.colors.cyan}进度:${this.colors.reset} [${this.colors.green}${bar}${this.colors.reset}] ${this.colors.yellow}${progress.toFixed(1)}%${this.colors.reset}`);
                
                if (!this.loopMode) {
                    const currentTime = this.getCurrentTime();
                    console.log(`${this.colors.cyan}时间:${this.colors.reset} ${this.colors.white}${this.formatTime(currentTime)}${this.colors.reset}`);
                }
            } else if (!this.playing && this.file) {
                console.log(`\n${this.colors.gray}⏸️ 暂停中...${this.colors.reset}\n`);
            } else if (this.songEnded && this.loopMode) {
                console.log(`\n${this.colors.green}🔄 等待下一轮循环...${this.colors.reset}\n`);
            } else {
                console.log(`\n${this.colors.gray}[ 无歌词 ]${this.colors.reset}\n`);
            }
        } else {
            console.log(`\n${this.colors.gray}[ 未播放 ]${this.colors.reset}\n`);
        }
        
        console.log(`${this.colors.gray}────────────────────────────────────────${this.colors.reset}`);
        if (this.file) {
            const statusIcon = this.playing ? `${this.colors.green}▶️${this.colors.reset}` : `${this.colors.yellow}⏸️${this.colors.reset}`;
            console.log(`${this.colors.cyan}状态:${this.colors.reset} ${statusIcon} ${this.playing ? '播放中' : '暂停'}`);
        }
        
        // 命令菜单
        console.log(`\n${this.colors.green}命令:${this.colors.reset}`);
        if (this.file) {
            console.log(`  ${this.colors.yellow}[p]${this.colors.reset}   暂停/继续`);
            console.log(`  ${this.colors.yellow}[l]${this.colors.reset}   循环模式 ${this.loopMode ? '(开启)' : '(关闭)'}`);
            console.log(`  ${this.colors.yellow}[s]${this.colors.reset}   停止`);
        } else {
            console.log(`  ${this.colors.yellow}[数字]${this.colors.reset} 选择音乐`);
        }
        console.log(`  ${this.colors.yellow}[q]${this.colors.reset}   退出`);
    }

    startAutoRefresh() {
        if (this.refreshInterval) clearInterval(this.refreshInterval);
        this.displayPlayer();
        this.refreshInterval = setInterval(() => {
            if (this.file) this.displayPlayer();
        }, 200);
    }

    async start() {
        process.stdin.setRawMode(true);
        process.stdin.resume();
        
        process.stdin.on('data', (data) => {
            const input = data.toString().trim();
            
            if (input === 'p' && this.file) {
                this.pause();
            } else if (input === 'l' && this.file) {
                this.toggleLoop();
            } else if (input === 's' && this.file) {
                this.stop();
                this.clearScreen();
            } else if (input === 'q') {
                this.running = false;
            } else if (/^\d+$/.test(input) && !this.file) {
                const files = this.listMusicFiles();
                const num = parseInt(input);
                if (num > 0 && num <= files.length) {
                    this.play(files[num-1]);
                }
            }
        });
        
        while (this.running) {
            if (!this.file) {
                this.clearScreen();
                console.log(`${this.colors.magenta}${this.colors.bold}🎵 歌词播放器${this.colors.reset}`);
                console.log(`${this.colors.gray}────────────────────────────────────────${this.colors.reset}`);
                console.log(`\n${this.colors.gray}[ 未播放 ]${this.colors.reset}\n`);
                
                const files = this.listMusicFiles();
                if (files.length) {
                    console.log(`${this.colors.cyan}📀 音乐文件:${this.colors.reset}`);
                    for (let i = 0; i < Math.min(10, files.length); i++) {
                        console.log(`   ${this.colors.yellow}${i+1}.${this.colors.reset} ${this.colors.white}${files[i]}${this.colors.reset}`);
                    }
                    console.log(`\n${this.colors.green}命令:${this.colors.reset} 输入数字选择音乐`);
                } else {
                    console.log(`${this.colors.red}❌ 没有音乐文件${this.colors.reset}`);
                }
                
                await new Promise(resolve => setTimeout(resolve, 100));
            } else {
                await new Promise(resolve => setTimeout(resolve, 100));
            }
        }
        
        this.stop();
        console.log(`\n${this.colors.yellow}👋 再见！${this.colors.reset}`);
        process.exit(0);
    }

    question(prompt) {
        return new Promise(resolve => {
            this.rl.question(prompt, resolve);
        });
    }
}

const player = new MusicPlayer();
player.start();