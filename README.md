# Weibo_Assistant

获取微博关注列表的变动记录。

## 功能

通过 cookies 登录微博，首次运行将获取当前的关注列表并保存至本地，下次运行会再次获取最新关注列表与本地数据进行比对，将变动内容发送至 Telegram Group 或 Channel。

## 配置

1. 使用 Chrome 浏览器登录 [微博 H5](https://m.weibo.cn/)，按 `F12` 打开 `开发者工具`，选择 `Network - XHR`，刷新页面，在 `m.weibo.cn - Headers - Request Headers` 中复制 `cookie` 的内容，粘贴至脚本自定义区域中的 `cookies_str`。
2. 在 `api_key` 中填写 Telegram Bot 的 `API Token`，可通过 [@BotFather](https://t.me/botfather) 获取。
3. 在 `chat_id` 中填写 Telegram 目标 Group 或 Channel 的 `chat id`（将 Telegram Bot 添加至 Group 或 Channel，然后发送一条消息，即可通过 `https://api.telegram.org/bot<YourBOTToken>/getUpdates` 获取当前 `chat id`）。

## 使用

推荐使用 Python3 运行。

需要安装以下内容

```shell
pip install python-telegram-bot requests
```

首次运行会在脚本同目录下创建 `weibo_follow_data.json` 用于保存数据。

可在服务器上配置 `crontab` 定时运行。

Example:

```crontab
0 */1 * * * python3 weibo_assistant.py # 每小时整点运行
```
