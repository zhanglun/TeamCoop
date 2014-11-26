## TeamCoop

### Flask 环境配置

Python 版本：2.7.6

参照官网的说明，使用`[virtualenv](http://dormousehole.readthedocs.org/en/latest/installation.html#virtualenv)`提供虚拟环境来避免版本兼容问题。

激活环境之后，安装Flask。


### 数据库文件使用说明
每次连接数据库时要先开启外键约束  
`pragma foreign_keys=on;`  
当做普通sql语句执行即可，不要忘了分号。