# API example

### This repo contains an app that shows how to:
### 1.  run a python script on a selected document at the click of a button
### 2. display the results of the script in the UI, and
### 3. export these results into a new PDF report

<hr>
This is a stripped down/shell app, posted here to serve as an example of API hosting functionalities (as well as basic interface/js functionalities). Special thanks to Doug Billings for his guidance in its creation.
<hr>

The app consists of 3 files:
* the UI (__`index.html`__) ------_note that all js code is contained in this file_
    * contains 2 xhttp functions (in javascript) that correspond to the server APIs
    * contains form for uploading the document (select file and submit buttons)
    * contains button to export PDF
* the python script (__`read_solicitation.py`__)
    * external python script contains the function to be run on the selected file
* the server (__`server.py`__)
    * contains 1 API to run the python script
    * contains 1 API to export the results as a PDF


In terminal, launch the app using:
`python3 server.py`


<hr>

### Let's review the app from the surface down, starting with the html content in __`index.html`__.

The __interactive part of the html__ consists of input buttons. First, inside `<form></form> tags, an input button allows the user to choose a file:
```html
<input type="file" id="myFile" name="solicitation_name">
```

The selected file is then fed to the function defined in the external python script using a submit button:
```html
<input class="btn btn-primary"
       value="Upload"
       onclick="run_py_script()"
       style="float:right; padding:2px; cursor: pointer;">
```

Once the content has been uploaded to the `<textarea>` with id="description", we can use another button to export the content to PDF:
```html
<input class="btn btn-primary" value="Download PDF of results" onclick="make_pdf_api()" style="cursor: pointer;">
```


In this example, all __javascript__ is containt within `<script></script>` tags inside the html file (__`index.html`__).


<hr>

### Running the external script

The function that runs the external script on the selected document is called `run_py_script()`, and uses an xhttp request to access the API on __`server.py`__.

```javascript
function run_py_script() {
   var url = location.origin + "/upload?file=" + document.getElementById("myFile").files[0].name;
   // console.log(url)
   var xhttp = new XMLHttpRequest();
   xhttp.onreadystatechange = function() {
      if (this.readyState == 4 && this.status == 200) {
         // console.log(this.responseText);
         document.getElementById("description").innerHTML = this.responseText;
      }
   };
   xhttp.open("GET", url, true);
   xhttp.send();
}
```

A url parameter (`?file=`) is used to specify that the function should run on the name of the file in the element with `id=myFile`. The file specified with `document.getElementById("myFile").files[0].name` is then accessed in the upload function from __`server.py`__ using `doc = request.args['file']`.

The result of the xhttp GET request (`this.responseText`) is the result of the api route function. In this case, the api route '/upload' runs the external function  `read_solicitation()`, imported at the top of the __`server.py`__ file. The responseText is sent to the `<textarea>` using the line `document.getElementById("description").innerHTML = this.responseText;`.


```python
from flask import Flask
from flask import request
from read_solicitation import read_solicitation

@app.route('/upload')
def upload():
    doc = request.args['file']
    print( "doc: ", doc)
    proj_descrip = read_solicitation(doc)
    print("description: ", proj_descrip)
    return proj_descrip
```

<hr>

### Exporting contents to PDF

To export the extracted text to a PDF, we use a js function. Note that in this case, the entire function is defined here and in the API -- no external script is accessed:

```javascript
function make_pdf_api() {
   var url = location.origin + "/pdf" ;
   console.log(url)
   var xhttp = new XMLHttpRequest();
   xhttp.onreadystatechange = function() {
      if (this.readyState == 4 && this.status == 200) {
         var file = new Blob([this.responseText], {type: 'application/pdf'});
         var fileURL = URL.createObjectURL(file);
         window.open(fileURL);
      }
   };
   // Report content:
   var payload= "<h1> THIS IS A NEW REPORT";
   payload += "</h1>";
   payload += "<h3> It shows the text extracted from the uploaded document, '";
   payload += document.getElementById("myFile").files[0].name;
   payload += "', in the space below: </h3>"
   payload += "<br>";
   payload += document.getElementById("description").innerHTML
   xhttp.open("POST", url, true);
   xhttp.send(payload);
}
```
This function also uses xhttp, but this time it is a POST request to avoid character limits. Notice also that `xhttp.send()` is now acting on the variable `payload`, which has been set to the PDF content. This conent is sent to the API route in __`server.py`__, which recieves it as `request.data` and writes it to a PDF using `pisa.CreatePDF()`. It then returns the response (`this.responseText`) in a new window (`window.open(fileURL)`) to display the PDF file created.

```python
from flask import Flask
from flask import send_file, request
from xhtml2pdf import pisa

@app.route('/pdf', methods=['POST'])
def make_pdf_api():
    html = request.data
    # print(html)
    f = open('report.pdf', 'wb')
    rc = pisa.CreatePDF(html, dest=f)
    f.close()
    return send_file('report.pdf')
```

From the new window, the PDF can be viewed, downloaded and/or printed.


<hr>
### important notes:
The file uploaded by the read_solicitation() function MUST be in the root directory of the app. 
