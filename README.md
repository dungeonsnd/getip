# getip
Get the target pc ip adress.

本项目用于获取另一网络中某台机器的内网和外网ip地址.


很多家庭宽带用户的ip地址是动态获取的，经常会发生变化，而且通常PC机等设备是通过路由器连上互联网的。 本项目的意义在于，可以在其它网络中随时获取到某局域网中PC机的内外网IP地址，有个内外网IP你可以做很多事情，比如可能通过VNC这样的软件去远程连接该局域网中的PC机(可能需要在路由上进行端口映射)。


项目中包含两个文件夹，即"go"和"python"，分别是两种编程语言的实现，但是目前只有python完成了完整功能并且作者已测试通过，可以正式使用。


项目包含三个应用，分别是IpCollector(见IpCollector文件夹), IpReport(见IpReport文件夹), IpAdmin(见IpAdmin.py)。


IpCollector是服务端，运行在公网服务器上，会启动一个udp服务。负责收集连接过来的客户端的内外网ip地址，并缓存到内存中，一段时间内没有收到某客户端的信息汇报会自动删除该客户端的缓存信息。 直接运行start_IpCollector.sh并回车，就可以后台运行IpCollector。


IpReport是客户端，运行在众多不同用户的PC机上(暂时只支持windows xp/win7/win8/win10 32位和64位系统，如果这些版本运行异常你可以向作者反馈)。 该应用软件会以windows后台服务的形式运行，自动定时向指定的服务器上汇报自己的网络地址。运行过程中定时读取名为C:/IpReport.txt的配置文件。配置文件内容使用json格式，其中比较重要的配置项是uid，指定你的身份信息，如果没有读取到则使用默认值，默认使用guid，你可以配置成任意和其它人不太容易重复的字符串，最好是你经常使用的邮箱，方便记忆也不会与他人冲突。

文件夹 getip/python/IpReport/dist 是客户端IpReport的发布文件，把dist这个文件夹拷贝到要运行客户端的目标PC机上，解压就可以了。其中的install.bat是安装后台服务，start.bat是启动后台服务。stop.bat是停止后台服务，remove.bat是卸载后台服务。


安装时把dist拷贝到目标机器上，然后运行(可能需要以管理员权限运行)install.bat和start.bat，安装之后可以在"计算机管理"-->"服务和应用程序"-->"服务"中看到类似"IpReport service"这样的服务，该服务就是本应用安装之后的服务。


拷贝IpReport.txt到C:/目录下。编辑C:/IpReport.txt文件(配置文件内容使用json格式)，把你的个人邮箱(或自定义的字符串)填写在{"uid":"","host":"mtzijin.com","port":"19601"}中uid冒号之后的位置。示例如下，{"uid":"dungeonsnd@gmail.com","host":"mtzijin.com","port":"19601"}。
改完以后，客户端就安装和配置完成了。然后可以在任意的机器上用 python IpAdmin.py "uid"来获取客户端机器的内外网IP地址了，示例如下，python IpAdmin.py dungeonsnd@gmail.com。



IpAdmin是管理端，用户想要获取IpReport所在机器的内外网ip地址时使用该管理端。使用时输入你在IpReport端配置的uid，就会从IpCollector立即取到uid对应机器的内外网ip地址。


如果返回下面的信息，表示客户端未正常运行，请检查客户端是否正常。
GET result:
   dungeonsnd@gmail.com not found!


如果返回下面的信息(json格式)，表示成功获取到客户端所在机器的内外网ip。localip表示内网ip, remoteip表示外网ip, lasttime表示服务器端IpCollector收到客户端IpReport最后心跳时间。
GET result:
   {u'localip': u"('192.168.23.95', 1174)", 'lasttime': 1428502899.223809, 'remoteip': ('58.240.26.203', 58557)}



