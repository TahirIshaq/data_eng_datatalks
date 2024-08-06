Details of the observations and challanges

## Host system details
While using AntiX Linux 23 which is based on Debian 12

```
lsb_release -a
No LSB modules are available.
Distributor ID:	Debian
Description:	Debian GNU/Linux 12 (bookworm)
Release:	12
Codename:	bookworm
```
## Docker related issues

### Docker engine not available
Before docker engine could not be installed for bookworm. Therefore, the version for bullseys had to be installed.

### Docker daemon not running

Even after manually starting the daemon starts but files when docker engine is run
`sudo service docker restart`
`sudo service docker status`

```
sudo apt update
sudo apt install cgroupfs-mount
sudo service docker stop
sudo cgroupfs-unmount
sudo cgroupfs-mount
sudo service docker restart
```

### DNS problem
Sometimes there is a DNS error. Not sure if it is docker specific. It is resolved be adding googles DNS
Open the DNS resolver file with edit permissions
`sudo nano /etc/resolv.conf`
Add google's DNS server address or edit the present DNS
`nameserver 8.8.8.8`


### Internet connection interference

Sometimes when running any docker service, the host computer becomes connected to the docker virtual internet connection. It only gets resolved when the host computers internet connection manager (connMan in this case) is reset.

Open the internet connection manager file with edit permissions
`sudo nano /etc/connman/main.conf`
Uncomment the line (if commented)
`NetworkInterfaceBlacklist = vmnet,vboxnet,virbr,ifb,ve-,vb-`
Add the following networks to this list:
`docker,veth`
Now reset the internet connection manager

## Pandas

- Pandas supports reading some compression types.

When trying to read a CSV file, the date columns need to passed in separately as a `list` in kwarg `parse_dates` and the remaining data types of columns in `dtype`. The date columns should not be included in `dtype` dictionary. All the columns were set to objects data type when I did this. The default pandas data types need to be set as `pd.Int64Dtype()` or `pd.Float64Dtype()` or `float` or any other size. Everything becomes a string/object if this [format](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.dtypes.html#pandas-dataframe-dtypes) is used.