from flask import Flask, request, send_file, render_template_string
from PIL import Image
import io

app = Flask(__name__)

    # This creates the visual layout of your website
HTML_PAGE = """
    <!DOCTYPE html>
    <html>
    <head>
        <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-9772284960841420"
     crossorigin="anonymous"></script>

        <title>Multi-Image to PDF</title>
        <style>
            body { font-family: sans-serif; text-align: center; padding: 50px; background-color: #f4f4f9; }
            .box { background: white; padding: 40px; border-radius: 10px; box-shadow: 0 4px 8px rgba(0,0,0,0.1); display: inline-block; }
            button { margin-top: 20px; padding: 12px 24px; background: #5c6bc0; color: white; border: none; border-radius: 5px; cursor: pointer; font-size: 16px; }
            button:hover { background: #3f51b5; }
        </style>
    </head>
    <body>
        <div class="box">
            <h2>🖼️ Convert Multiple Images to PDF</h2>
            <form action="/convert" method="post" enctype="multipart/form-data">
                <p>Select your JPG or PNG files:</p>
                <input type="file" name="images" multiple accept="image/png, image/jpeg, image/jpg" required>
                <br>
                <button type="submit">Convert to PDF</button>
            </form>
        </div>
    </body>
    </html>
    """

@app.route('/')
def home():
        return render_template_string(HTML_PAGE)

@app.route('/convert', methods=['POST'])
def convert():
        # Grab all the uploaded files
        files = request.files.getlist('images')
        
        if not files or files[0].filename == '':
            return "Please select at least one image.", 400
        
        image_list = []
        first_image = None
        
        # Process each picture one by one
        for file in files:
            try:
                img = Image.open(file).convert('RGB')
                if first_image is None:
                    first_image = img
                else:
                    image_list.append(img)
            except Exception as e:
                print(f"Skipped an invalid file: {e}")
                
        if first_image is None:
            return "No valid images found.", 400

        # Bundle them all together into a PDF in the computer's memory
        pdf_bytes = io.BytesIO()
        first_image.save(pdf_bytes, format='PDF', save_all=True, append_images=image_list)
        pdf_bytes.seek(0)
        
        # Send the finished PDF back to the user's browser
        return send_file(pdf_bytes, download_name='my_converted_images.pdf', as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
