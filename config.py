path="/home/dot/scripts/cpu_governor"
if path.endswith("/"):
    path=path[:-1]
commands=[
    {"start":"/usr/bin/echo '","args":["conservative","performance","powersave","ondemand","schedutil"],"end":"' | /usr/bin/tee /sys/devices/system/cpu/cpu*/cpufreq/scaling_governor"},
    {"start":f"/usr/bin/cp {path}/tlp_","args":["conservative","default","performance","powersave","ondemand","schedutil"],"end":".conf /etc/tlp.conf"},
    {"start":"/usr/bin/systemctl ","args":["restart "],"end":"tlp"}
]

current = set()
CPUs_dir = "/sys/devices/system/cpu/"
cpu_file="cpufreq/scaling_governor"
tlp_restart="/usr/bin/systemctl restart tlp"
cp_format="/usr/bin/cp %source %destination"
tlp_default="tlp_default.conf"
# startup_combo=None
startup_combo=0
wait_on_startup=0.75

