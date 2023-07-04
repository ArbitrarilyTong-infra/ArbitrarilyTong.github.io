# 屎山GIT仓库批量管理程序——REPO 使用指北
## 什么是repo？
来自Google官方的介绍：

>Repo is a tool built on top of Git. Repo helps manage many Git repositories, does the uploads to revision control systems, and automates parts of the development workflow. Repo is not meant to replace Git, only to make it easier to work with Git. The repo command is an executable Python script that you can put anywhere in your path.

简单的说就是一个批量管理Git仓库的程序，尽管Google宣称 "make it easier to work with Git" 但实际上可以说使用体验一坨屎

本文档将会介绍repo工具的一些常见问题并提供解决办法

## 常见问题&解决办法
### xxx仓库同步最新上游仓库时更新失败 
属于该类问题的错误日志包括：
 - cannot checkout （目录名）
 - ManifestInvalidRevisionError
 - fatal: bad object (一大串commit id)
解决办法:
打开项目根目录下面的 `.repo` 目录，你会看到有 `projects` 和 `project-objects`
在这两个目录里面删掉同步失败的目录，例如：
![](https://arbitrarilytong.win/img/guide/screenshots/photo_2023-07-04_04-17-22.jpg)
删除完毕后再重新同步即可
![](https://arbitrarilytong.win/img/guide/screenshots/photo_2023-07-04_04-19-34.jpg)