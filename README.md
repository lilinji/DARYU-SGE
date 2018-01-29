# DAYU-SGE
用于安装SGE-HPC集群在阿里云ECS
# AdminSet
<img src="https://travis-ci.org/guohongze/adminset.svg?branch=master"></img> 
<img src="https://img.shields.io/hexpm/l/plug.svg"></img>
[![release](https://img.shields.io/github/release/guohongze/adminset.svg)](https://github.com/lilinji/DAYU-SGE/Aliyun-Novogene-SGE)
<br>
DAYU-SGE基于DevOps理念开发，以整合全部运维场景为己任。DAYU-SGE是一个真正的基于运维思维而开发的全自动化安装集群Pipline。<br>

## v1.0.1 新功能
自动安装 master 主机.<br>
自动安装 compute 计算节点.<br>
自动下载源码 SGE.<br>
自动安装 SGE.<br>
自动配置 队列.<br>
自动配置 主机组.<br>
自动配置 优化.<br>

## 开发环境
centos 7.4(1708)  vim （兼容 Notes） python 2.7 兼容（3.4）<br>

## 服务端安装
生产服务器建议 4核CPU，8G内存以上.<br>
学习测试建议 2核CPU，2G内存以上.<br>
服务器操作系统版本要求 centos7.2及以上<br>
安装过程不需要任何操作<br>
```
git clone https://github.com/lilinji/DAYU-SGE.git
```

## 客户端安装
客户端脚本目前rhel/centos6、7,ubuntu14.04经过测试<br>
客户端python版本支持2.6.6及以上<br>
说明：为保证注册IP是管理IP（后续会被epel等调用），客户端的保证与主机在同一网络。保证当前节点能上网 
如：主机名为master  请在/etc/hosts中查看相应的解析 192.168.x.x master，这样再执行run.sh 可以保证正常运行。
#### step1:
拷贝源码到管理主机上并执行:
```
cd Aliyun-Novogene-SGE
vim  host 确保 头节点在第一行 
192.168.x.x      #头节点IP 
192.168.1.2      #计算节点
192.168.1.3      #计算节点
192.168.1.4      #计算节点
```
#### step2:
到当前主机上并执行:
```
sh run.sh
```
后台运行请参考：
```
nohup sh run.sh >run.sh.nohuop 2>run.sh.error &
```

## 访问
https://github.com/lilinji/DAYU-SGE.git 


## 说明
使用请转到，<a href="https://github.com/lilinji/DAYU-SGE/blob/master/Aliyun-Novogene-SGE/README">使用说明</a><br>
功能请转到，<a href="https://github.com/lilinji/DAYU-SGE/blob/master/Aliyun-Novogene-SGE/conf.py">功能说明</a><br>
FAQ请转到，<a href="https://www.baidu.com">常见问题</a>

# 安全
要将程序启动在有公网可以直接访问的设备上<br>
建议生产环境中使用https配置服务器<br>
由于开发方便，在ptython的settings中开启了DEBUG，在生产中需要关闭并指定自己的域名。

# 开发者交流
请加入开发者群，注明来自github
<img src="https://github.com/lilinji/DAYU-SGE/blob/master/Aliyun-Novogene-SGE/1.png"></img>
