import datetime, os, random, string, shutil, time

from sanic import response, Sanic
from sanic.log import logger
from sanic.request import RequestParameters

import boto3

from faceFactory import face_cropper

app = Sanic()
args = RequestParameters()

@app.route("/", methods=['GET','POST'])
async def test(request):
    return response.html('''<form method=POST enctype=multipart/form-data action"http://0.0.0.0:8000/image">
            <input type=file name="image">
            <input type=submit>
            </form>''')

@app.route("/image", methods=['POST'])
async def handle_upload(request):
    ts = time.time()
    timestamp = datetime.datetime.fromtimestamp(ts).strftime('%Y%m%d%H%M%S')
    upload_id = ''.join(random.choices(string.ascii_lowercase + string.digits, k=7)) + "_" + timestamp

    #image = request.files.get('image')
    #logger.info(f"{image.name}")

    s3 = boto3.client('s3')
    bucket_name = os.environ.get('BUCKET_NAME')
    
    # Temporary workaround, write directories and files locally to ship to S3
    outdir = f"images/output/{upload_id}"
    updir = f"images/upload"
    if not os.path.exists(outdir):
        os.makedirs(outdir)

    # Write incoming image locally, send to S3
    image_file = f"./{updir}/{upload_id}.jpg"
    with open(image_file,'wb') as fileout:
        fileout.write(request.files.get('image').body) 
    s3.put_object(Bucket=bucket_name, Key=f'{updir}/{upload_id}.jpg', Body=open(image_file, 'rb'))
    
    # OpenCV will statistically guesstimate faces, crop and write them locally
    cropper = face_cropper.FaceCropper(f"./{outdir}")
    cropper.process_image(image_file)

    # Read local output 'face' images and ship to S3
    for output_image in os.listdir(f"./{outdir}"):
        s3.put_object(Bucket=bucket_name, Key=f'{outdir}/{output_image}', Body=open(f"./{outdir}/{output_image}", 'rb'))
        
    # Local file and directory cleanup
    for path in ["./images/output/",f"{updir}"]:
        for output_file in os.listdir(path):
            file_path = os.path.join(path, output_file)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path): shutil.rmtree(file_path)
            except Exception as e:
                print(e)
    
    return response.text("testing image route")

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=8000)
