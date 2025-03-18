# 安装编译
## 基本环境
sudo apt-get install -y build-essential cmake autoconf

## 安装 libpcap
sudo apt-get install -y flex bison
wget https://www.tcpdump.org/release/libpcap-1.10.1.tar.gz
tar -xzf libpcap-1.10.1.tar.gz
cd libpcap-1.10.1/
./configure --prefix=/usr
make -j2
sudo make install

## 安装 libdaq
sudo apt-get install -y pkg-config libtool libmnl-dev nftables

git clone https://github.com/snort3/libdaq.git --branch v3.0.5 --depth 1
cd libdaq/
./bootstrap
./configure --prefix=/usr
make -j2
sudo make install

## 安装 libdnet
git clone --depth 1 https://github.com/ofalk/libdnet.git
cd libdnet/
./configure --prefix=/usr
make -j2
sudo make install

## 安装snort

sudo apt-get install -y libhwloc-dev luajit libluajit-5.1-dev libssl-dev libpcre3-dev zlib1g-dev liblzma-dev libunwind-dev uuid-dev libhyperscan-dev libflatbuffers-dev libsafec-dev libjemalloc-dev
git clone https://github.com/snort3/snort3.git --branch 3.1.19.0 --depth 1
cd snort3
./configure_cmake.sh --prefix=/usr/local --enable-jemalloc
cd build/
make -j2
sudo make install

## 测试是否安装成功
snort -V

# ------------------------------------------------------------------------------

# 设置网络接口
sudo ethtool -k ens33 | grep receive-offload
sudo vi /lib/systemd/system/ethtool.service
##内容，输入以下信息，用接口名称替换ens3：
[Unit]
Description=Ethtool Configration for Network Interface
[Service]
Requires=network.target
Type=oneshot
ExecStart=/sbin/ethtool -K ens33 gro off
ExecStart=/sbin/ethtool -K ens33 lro off
[Install]
WantedBy=multi-user.target
##:wq
# 设置上方开机自启
sudo systemctl enable ethtool
sudo service ethtool start

# 配置规则文件夹
sudo mkdir /usr/local/etc/rules
sudo mkdir /usr/local/etc/so_rules/
sudo mkdir /usr/local/etc/lists/
sudo touch /usr/local/etc/rules/snort.rules
sudo touch /usr/local/etc/rules/local.rules
sudo touch /usr/local/etc/lists/default.blocklist
sudo mkdir /var/log/snort
# 编辑规则
sudo vi /usr/local/etc/rules/local.rules
##内容
alert icmp any any -> any any ( msg:"ICMP Traffic Detected"; sid:10000001; metadata:policy security-ips alert; )
##:wq
# 启动snort抓取ens33接口的ICMP流量
snort -c /usr/local/etc/snort/snort.lua -R /usr/local/etc/rules/local.rules
sudo snort -c /usr/local/etc/snort/snort.lua -R /usr/local/etc/rules/local.rules \
-i ens33 -A alert_fast -s 65535 -k none


# 将日志以json格式保存到文件中
sudo vim /usr/local/etc/snort/snort.lua
##内容
alert_json =
{
    file = true,
    limit = 100,
    fields = 'seconds action class b64_data dir dst_addr dst_ap dst_port eth_dst eth_len \
    eth_src eth_type gid icmp_code icmp_id icmp_seq icmp_type iface ip_id ip_len msg mpls \
    pkt_gen pkt_len pkt_num priority proto rev rule service sid src_addr src_ap src_port \
    target tcp_ack tcp_flags tcp_len tcp_seq tcp_win tos ttl udp_len vlan timestamp',

}
##:%wq
snort -c /usr/local/etc/snort/snort.lua -R /usr/local/etc/rules/log.rules
sudo snort -c /usr/local/etc/snort/snort.lua -R /usr/local/etc/rules/log.rules \
-i ens33 -s 65535 -k none -l /var/log/snort -m 0x1b


# TCP所有日志
sudo snort -c /usr/local/etc/snort/snort.lua -R /usr/local/etc/rules/log.rules \
-i ens33 -s 65535 -k none -l /var/log/snort/log -m 0x1b

# 触发规则日志
sudo snort -c /usr/local/etc/snort/snort.lua -R /usr/local/etc/rules/detection.rules \
-i ens33 -s 65535 -k none -l /var/log/snort/detect -m 0x1b

