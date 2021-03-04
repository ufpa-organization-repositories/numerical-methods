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
                
                let buttonMethodEl = this.renderMethodButton(method);

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

    renderMethodButton = (method) => {
        // way 01: DOM
        // let buttonChapterEl = document.createElement("button");
        // buttonChapterEl.type = "submit";
        // buttonChapterEl.value = chapter;
        // buttonChapterEl.name = "chapter";
        // buttonChapterEl.innerText = chapter;

        // let brEl = document.createElement("br");
        // buttonChapterEl.append(brEl);

        // way 02: template string
        let chapterEl = document.createElement("div");
        chapterEl.setAttribute("class", "button-div");
        chapterEl.innerHTML = `<button class="button-elem" type="submit" value="${method}" name="method">${method}</button>`;
        return chapterEl;

    }

}