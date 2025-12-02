# Hướng dẫn cấu hình AWS Credentials

## Cách 1: Sử dụng AWS CLI (Khuyên dùng)

### Bước 1: Cài đặt AWS CLI

```bash
# macOS
brew install awscli

# Linux
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip
sudo ./aws/install
```

### Bước 2: Cấu hình credentials

```bash
aws configure
```

Nhập thông tin khi được hỏi:

- AWS Access Key ID: `YOUR_ACCESS_KEY`
- AWS Secret Access Key: `YOUR_SECRET_KEY`
- Default region name: `ap-southeast-1`
- Default output format: `json`

## Cách 2: Tạo file credentials thủ công

### Tạo thư mục và file

```bash
mkdir -p ~/.aws
nano ~/.aws/credentials
```

### Nội dung file ~/.aws/credentials

```ini
[default]
aws_access_key_id = YOUR_ACCESS_KEY
aws_secret_access_key = YOUR_SECRET_KEY
```

### Tạo file config (tùy chọn)

```bash
nano ~/.aws/config
```

```ini
[default]
region = ap-southeast-1
output = json
```

## Cách 3: Sử dụng biến môi trường (Cho Cloud Shell)

### Trên Linux/macOS

```bash
export AWS_ACCESS_KEY_ID="YOUR_ACCESS_KEY"
export AWS_SECRET_ACCESS_KEY="YOUR_SECRET_KEY"
export AWS_DEFAULT_REGION="ap-southeast-1"
```

### Thêm vào file start.py (nếu cần)

```python
import os
os.environ['AWS_ACCESS_KEY_ID'] = 'YOUR_ACCESS_KEY'
os.environ['AWS_SECRET_ACCESS_KEY'] = 'YOUR_SECRET_KEY'
os.environ['AWS_DEFAULT_REGION'] = 'ap-southeast-1'
```

## Kiểm tra cấu hình

```bash
# Kiểm tra credentials
aws sts get-caller-identity

# Kiểm tra kết nối Bedrock
aws bedrock-agent-runtime list-knowledge-bases --region ap-southeast-1
```

## Lưu ý bảo mật

- KHÔNG commit credentials vào Git
- KHÔNG share credentials với người khác
- Sử dụng IAM roles khi có thể
- Rotate credentials định kỳ

## Permissions cần thiết

IAM User cần có các quyền sau:

- `bedrock:InvokeModel`
- `bedrock:RetrieveAndGenerate`
- `bedrock:Retrieve`
- `s3:GetObject` (cho Knowledge Base)

## Troubleshooting

### Lỗi "Unable to locate credentials"

- Kiểm tra file ~/.aws/credentials tồn tại
- Kiểm tra format file đúng
- Thử chạy `aws configure` lại

### Lỗi "AccessDeniedException"

- Kiểm tra IAM permissions
- Đảm bảo region đúng (ap-southeast-1)
- Kiểm tra Knowledge Base ID đúng

### Lỗi "ExpiredToken"

- Credentials đã hết hạn
- Cần tạo credentials mới từ AWS Console
