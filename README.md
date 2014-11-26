## TeamCoop

### Flask 环境配置

Python 版本：2.7.6

参照官网的说明，使用`[virtualenv](http://dormousehole.readthedocs.org/en/latest/installation.html#virtualenv)`提供虚拟环境来避免版本兼容问题。

激活环境之后，安装Flask。


### 数据库文件使用说明
为了使外键约束生效，在每次连接数据库时要限制性一次`pragma foreign_keys=on;`指令，不要少了分号。