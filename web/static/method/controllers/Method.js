class Method {

    constructor () {
        this.logTableEl = document.querySelector(".table");
        this.initialize();
    }

    initialize(){
        this.getLog();
    }

    getLog(){        
        this.httpGetAsync('http://127.0.0.1:5000/log', (response) => {
	        let obj = JSON.parse(response);            
            obj.log.forEach( (info, index) => {
                // https://www.w3schools.com/js/js_htmldom_nodes.asp#:~:text=To%20add%20text%20to%20the,is%20a%20new%20paragraph.%22)%3B                
                let trEl = document.createElement("tr");
                let tdEl = document.createElement("td");
                                
                let textNode = document.createTextNode(info);
                tdEl.appendChild(textNode);
                trEl.appendChild(tdEl);
                this.logTableEl.appendChild(trEl);
            });
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