# 微信 Linux 版本历史

自动跟踪[微信 Linux 版](https://linux.weixin.qq.com/)的公开版本历史。

## 支持的平台与格式

| 架构 | deb | rpm | AppImage |
|------|-----|-----|----------|
| x86_64 | ✅ | ✅ | ✅ |
| arm64 | ✅ | ✅ | ✅ |
| LoongArch | ✅ | — | — |

## 下载地址

- **x86_64**: [deb](https://dldir1v6.qq.com/weixin/Universal/Linux/WeChatLinux_x86_64.deb) / [rpm](https://dldir1v6.qq.com/weixin/Universal/Linux/WeChatLinux_x86_64.rpm) / [AppImage](https://dldir1v6.qq.com/weixin/Universal/Linux/WeChatLinux_x86_64.AppImage)
- **arm64**: [deb](https://dldir1v6.qq.com/weixin/Universal/Linux/WeChatLinux_arm64.deb) / [rpm](https://dldir1v6.qq.com/weixin/Universal/Linux/WeChatLinux_arm64.rpm) / [AppImage](https://dldir1v6.qq.com/weixin/Universal/Linux/WeChatLinux_arm64.AppImage)
- **LoongArch**: [deb](https://dldir1v6.qq.com/weixin/Universal/Linux/WeChatLinux_LoongArch.deb)

## [`versions.json`](versions.json)

此文件记录微信 Linux 版的版本历史，结构如下：

```json
[
    {
        "released": "<ISO8601 格式的发布日期>",
        "size": "<安装包大小（字节）>",
        "md5": "<安装包 MD5>",
        "version": "<版本号>"
    }
]
```

## 工作原理

通过 GitHub Actions 定时检测 x86_64 deb 包的 `Last-Modified` 响应头来判断是否有新版本发布。检测到更新后，自动下载所有平台的安装包并记录版本信息。

## 相关项目

- [WeChat4-Version-History](https://github.com/PRO-2684/WeChat4-Version-History)：自动跟踪微信 Windows 版的版本历史。
