import streamlit as st
import boto3
import time
from botocore.exceptions import NoCredentialsError, ClientError
from botocore.config import Config

# Cấu hình AWS Bedrock
KB_ID = "KQCHKPPDTV"
MODEL_ARN = "arn:aws:bedrock:us-east-1::foundation-model/anthropic.claude-3-5-sonnet-20240620-v1:0"
REGION = "us-east-1"

# Cấu hình retry với backoff để tránh throttling
retry_config = Config(
    retries={
        'max_attempts': 10,
        'mode': 'adaptive'
    }
)

# Khởi tạo Bedrock client với retry config
try:
    client = boto3.client(
        service_name='bedrock-agent-runtime',
        region_name=REGION,
        config=retry_config
    )
    sts = boto3.client('sts', region_name=REGION)
    sts.get_caller_identity()
except NoCredentialsError:
    st.error("LOI: Khong tim thay AWS credentials")
    st.info("""
    Cau hinh AWS credentials bang cach chay lenh:
    
    ```bash
    aws configure
    ```
    
    Hoac tao file ~/.aws/credentials voi noi dung:
    
    ```
    [default]
    aws_access_key_id = YOUR_ACCESS_KEY
    aws_secret_access_key = YOUR_SECRET_KEY
    ```
    """)
    st.stop()
except Exception as e:
    st.error(f"LOI ket noi AWS: {str(e)}")
    st.stop()

# Cấu hình trang
st.set_page_config(
    page_title="Vicobi Chatbot",
    page_icon="💬",
    layout="centered"
)
st.title("Chatbot AWS Bedrock")
st.caption("Hỏi đáp với Knowledge Base")

# Khởi tạo lịch sử chat và rate limiting
if "messages" not in st.session_state:
    st.session_state.messages = []
if "last_request_time" not in st.session_state:
    st.session_state.last_request_time = 0

# Hiển thị lịch sử chat lên màn hình
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Xử lý câu hỏi từ người dùng
if prompt := st.chat_input("Nhập câu hỏi của bạn..."):
    # Rate limiting: Đảm bảo tối thiểu 2 giây giữa các request
    time_since_last = time.time() - st.session_state.last_request_time
    if time_since_last < 2:
        st.warning(f"Vui long doi {2 - time_since_last:.1f} giay truoc khi gui cau hoi tiep theo")
        st.stop()
    
    st.session_state.last_request_time = time.time()
    
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        message_placeholder.markdown("Đang xử lý...")

        try:
            response = client.retrieve_and_generate(
                input={'text': prompt},
                retrieveAndGenerateConfiguration={
                    'type': 'KNOWLEDGE_BASE',
                    'knowledgeBaseConfiguration': {
                        'knowledgeBaseId': KB_ID,
                        'modelArn': MODEL_ARN
                    }
                }
            )

            answer = response['output']['text']

            # Hiển thị nguồn tài liệu
            if 'citations' in response and response['citations']:
                citations = response['citations'][0]['retrievedReferences']
                if citations:
                    doc_uri = citations[0]['location']['s3Location']['uri']
                    doc_name = doc_uri.split('/')[-1]
                    answer += f"\n\n---\nNguon: {doc_name}"

            message_placeholder.markdown(answer)
            st.session_state.messages.append({"role": "assistant", "content": answer})

        except NoCredentialsError:
            message_placeholder.error("Loi: Khong tim thay AWS credentials. Vui long cau hinh AWS CLI.")
        except ClientError as e:
            error_code = e.response['Error']['Code']
            if error_code == 'ThrottlingException':
                message_placeholder.warning("""
                Loi: Qua nhieu yeu cau trong thoi gian ngan
                
                Vui long:
                - Doi 5-10 giay truoc khi thu lai
                - Tranh gui nhieu cau hoi lien tiep
                - Kiem tra xem co tab hoac cua so nao khac dang chay cung luc khong
                """)
            elif error_code == 'ResourceNotFoundException':
                message_placeholder.error(f"""
                Loi: Knowledge Base khong ton tai!
                
                Knowledge Base ID: {KB_ID}
                Region: {REGION}
                
                Huong dan kiem tra:
                1. Truy cap AWS Console > Bedrock > Knowledge Bases
                2. Kiem tra Knowledge Base ID chinh xac
                3. Dam bao Knowledge Base o region: {REGION}
                4. Cap nhat KB_ID va REGION trong file app.py
                """)
            else:
                message_placeholder.error(f"Loi AWS: {error_code} - {str(e)}")
        except Exception as e:
            message_placeholder.error(f"Loi: {str(e)}")
