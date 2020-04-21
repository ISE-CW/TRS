import oss2


def upload_pic(path):
    access_key_id = 'LTAI4GK51z5hUZYRtucuRFpu'
    access_key_secret = '1mxjE6jk6WyFZGiPCMtFn1ElOGPHIw'
    bucket_name = 'ise-trs'
    endpoint = 'oss-cn-shanghai.aliyuncs.com'
    # 创建对象
    bucket = oss2.Bucket(oss2.Auth(access_key_id, access_key_secret), endpoint, bucket_name)
    # 上传
    tmp = path.split('\\')
    pic_name = tmp[len(tmp)-1]
    with open(path, "rb") as f:
        data = f.read()
    bucket.put_object(pic_name, data)  # data为数据，可以是图片
    url = bucket.sign_url('GET', pic_name, 60 * 60 * 24)  # 返回值为链接，参数依次为，方法/oss上文件路径/过期时间(s)
    return url
