# 🐍💬 pyhon-encrypted-chat
#### [python 3.8.5]
Python socket Server-Client application capable of handling multiple connections and **Asymmetric Encryption** of data streams. <br/>
This chat consists of two files and a tcp-socket communication library that I wrote.

## How To Start:
#### 📩 Please install all the dependencies by running:
```python
pip install -r requirements.txt
```

#### 🆘 To get the list of all available arguments - type:
```python
python server.py --help
python client.py --help
```

#### 🏃‍♂ To start server / client:
```python
python server.py -a <IP> -p <PORT> --verbose
python client.py -a <IP> -p <PORT> --verbose
```

## Argumets:
None of arguments are required to run either server or client.
If run without options - defaults will be used.

#### 💿 Options [server | client]:
<pre>
-a  --ip-address   default = 127.0.0.1
-p  --port         default = 5000     
</pre>

#### 🚩 Flags [server | client]:
<pre>
-v  --verbose      default = True     
</pre>
