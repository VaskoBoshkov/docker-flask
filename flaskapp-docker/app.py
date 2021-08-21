from create_bucket import create_bucket
from urllib import request
import boto3
from flask import Flask, render_template, request, redirect, send_file

s3 = boto3.client('s3')
app = Flask(__name__)

@app.route("/")
def home():
    return render_template('index.html')

@app.route("/upload", methods=['POST'])
def upload():
    if request.method == "POST":
        f = request.files['file']
        bucket_name = f"filetype-{f.filename.split('.')[-1]}"
        # Retrieve the list of existing buckets

        buckets = s3.list_buckets()
        in_bucket = False

        # Output the bucket names
        for bucket in buckets['Buckets']:
            if bucket_name in bucket["Name"]:
                s3.put_object(Bucket=bucket_name, Key=f"{f.filename}", Body=f.filename,
                              ServerSideEncryption='aws:kms')
                in_bucket = True
                break
        if not in_bucket:
            create_bucket(bucket_name)
            s3.put_object(Bucket=bucket_name, Key=f"{f.filename}", Body=f.filename,
                          ServerSideEncryption='aws:kms')
        return redirect("/")


if __name__ == '__main__':
    app.run(debug=True)
