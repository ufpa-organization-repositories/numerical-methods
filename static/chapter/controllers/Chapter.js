class Chapter {
    
    constructor () {
        this.formEl = document.querySelector("#methods");        
        this.initialize();
    }

    initialize(){        
        this.getMethods();
    }

    getMethods(){        
        this.httpGetAsync('http://127.0.0.1:5000/methods', (response) => {
	        let obj = JSON.parse(response);
            obj.methods.forEach((method, index) => {
                console.log(index, method);                
                
                // https://www.w3schools.com/jsref/met_document_createelement.asp
        
                let buttonMethodEl = document.createElement("button");
                buttonMethodEl.type = "submit";
                buttonMethodEl.value = method;
                buttonMethodEl.name = "method";
                buttonMethodEl.innerText = method;

                let brEl = document.createElement("br");
                buttonMethodEl.append(brEl);

                this.formEl.appendChild(buttonMethodEl);

            });
            // console.log(this.formEl);
        });    
    }
        
    httpGetAsync(theUrl, callback) {   
        var xmlHttp = new XMLHttpRequest();
        xmlHttp.onreadystatechange = function() {
            if (xmlHttp.readyState == 4 && xmlHttp.status == 200)
                callback(xmlHttp.responseText);            
            }
            
        xmlHttp.open("GET", theUrl, true); // true for asynchronous
        xmlHttp.send(null); // https://developer.mozilla.org/pt-BR/docs/Web/API/XMLHttpRequest/send 
    }    

}