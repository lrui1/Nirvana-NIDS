ips =
{
    enable_builtin_rules = true,
    rules = [[
        include /usr/local/etc/rules/detect/sqlInjection.rules
        include /usr/local/etc/rules/detect/xss.rules
        include /usr/local/etc/rules/detect/fileUpload.rules
        include /usr/local/etc/rules/detect/rce.rules
        include /usr/local/etc/rules/detect/dir.rules
    ]],
    variables = default_variables
}

custom_classifications = {
    { name = 'TCP流量记录', priority = 1,
      text = 'TCP流量记录' },
    { name = 'SQL注入攻击', priority = 3,
      text = 'SQL注入攻击' },
    { name = 'XSS注入攻击', priority = 2,
      text = 'XSS注入攻击' },
    { name = '文件上传攻击', priority = 3,
      text = '文件上传攻击' },
    { name = '命令执行攻击', priority = 4,
      text = '命令执行攻击' },
    { name = '目录遍历攻击', priority = 2,
      text = '目录遍历攻击' }
}

# 启动
# detect
sudo snort -c /usr/local/etc/snort/snort-detect.lua \
-i ens33 -s 65535 -k none -l /var/log/snort/detect -m 0x1b
# HTTP
sudo snort -c /usr/local/etc/snort/snort-log.lua -R /usr/local/etc/rules/log.rules \
-i ens33 -s 65535 -k none -l /var/log/snort/log -m 0x1b



# RCE
sudo snort -c /usr/local/etc/snort/snort.lua -R /usr/local/etc/rules/detect/sqlInjection.rules \
-i ens33 -s 65535 -k none -l /var/log/snort/detect -m 0x1b
