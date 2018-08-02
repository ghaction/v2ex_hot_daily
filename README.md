# v2ex每日热点列表
>抓取并保存了[v2ex](https://www.v2ex.com/)的每日热点列表，按年月日保存成markdown文件。

## 安装
首先clone代码到本地，然后使用pipenv安装依赖。

```bash
git clone git@github.com/w169q169/v2ex_hot_daily
cd v2ex_hot_daily
pipenv sync

pipenv run python main.py

```

## 其他

### git_push.sh
这个脚本可以将抓取后的数据push到github或者其他远程仓库。
```bash
bash git_push.sh
```

### crontab示例
```
# 每日8点、16点、23点的45分时，抓取数据并提交到github上
45 8,16,23 * * * cd /root/tool/v2ex-host-daily && bash git_push.sh >> /tmp/push.log 2>&1
```


