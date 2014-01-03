javascript:(
    function(){
        function copyToClipboard(text){
            window.prompt("Copy to clipboard: Ctrl+C, Enter",text);
        }
        var xhr=new XMLHttpRequest();
        xhr.onload=function(e){
            if(this.status==200){
                var xhr2=new XMLHttpRequest();
                xhr2.onreadystatechange=function(){
                    switch(xhr2.readyState){
                        case 0:
                        case 1:
                        case 2:
                        case 3:
                            break;
                        case 4:
                            if(xhr2.status==200){
                                //copyToClipboard(xhr2.responseText);
                                document.getElementsByTagName("html")[0].innerHTML = (xhr2.responseText);
                            }
                            else if(xhr2.status!=200){
                                alert('upload failure, status code '+xhr2.status);
                            }
                            break;
                        default:
                            alert('bad readyState value');
                    }
                };
                xhr2.open('POST','http://diyhpl.us:5000/~nmz787/addpdf',true);
                xhr2.setRequestHeader('crossDomain','true');
                var formData=new FormData();
                formData.append('file',xhr.response);
                var filename=prompt('Please enter a different filename if you like',window.location.pathname.split('/')[window.location.pathname.split('/').length-1]);
                if(filename==null){return;}
                if(filename.indexOf('.pdf')==-1){filename+='.pdf';}
                formData.append('filename',filename);
                formData.append('url',window.location);
                formData.append('contentType',xhr.getResponseHeader('content-type'));
                xhr2.send(formData);
            }
        };
        xhr.open('GET',window.location,true);
        xhr.responseType='blob';
        xhr.send(null);
    }
)();