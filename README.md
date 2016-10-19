
rsshub
======

最后一个 rss 管理软件


## TODO

- [x] 添加 RSS
- [x] 用户订阅 RSS
- [x] 更新 RSS
- [x] RSS 生成 mobi 文件
- [x] 生成 mobi 文件 推送到 Kindle
- [ ] 允许用户自定义邮件地址
- [ ] 生成的 mobi 文件支持显示图片
- [ ] 多用户同时构建 mobi
- [ ] cron 更新 RSS

## CRON
~~~bash
/home/phyng/project/rsshub/env/bin/python /home/phyng/project/rsshub/manage.py update_rss
~~~
