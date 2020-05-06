import tempfile
from pathlib import Path

import boto3
from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename

app = Flask(__name__)

UPLOAD_BUCKET_NAME = 'upload_bucket'


@app.route('/upload', methods=['POST'])
def upload_file():
    s3 = boto3.resource('s3')
    bucket = s3.Bucket(UPLOAD_BUCKET_NAME)
    if len(request.files) == 0:
        return jsonify({'message': 'No file received'}), 400
    files_to_upload = request.files
    objects = []
    for file_name in files_to_upload:
        file = files_to_upload[file_name]
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_dir_file_path = Path(temp_dir) / file.filename
            file.save(temp_dir_file_path)
            with open(temp_dir_file_path, 'r') as f:
                object_ = bucket.put_object(
                    Key=secure_filename(file.filename),
                    Body=f.read(),
                    ContentType=file.content_type,
                )
                objects.append(object_.key)
    return jsonify({'message': 'Files successfully uploaded', 'objects_uploaded': objects}), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
