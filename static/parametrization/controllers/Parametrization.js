class Parametrization {
    // https://wesbos.com/template-strings-html

    constructor () { 
        this.formEl = document.querySelector(".form");
        this.initialize();
    }

    initialize(){        
        this.getParameters();        
    }

    addParametersAndSubmit(parametersObj){

        // parameters
        for (let param in parametersObj){
            let paramEl = this.renderTextInput(param);
            this.formEl.appendChild(paramEl);
        }

        // submit
        let submitEl = this.renderSubmit();
        this.formEl.appendChild(submitEl);

    }

    getParameters(){        
        this.httpGetAsync('http://127.0.0.1:5000/parameters', (response) => {
	        let obj = JSON.parse(response);            
            this.addParametersAndSubmit(obj)
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

    // Templates

    renderTextInput = (param) => {        
        let paramEl = document.createElement("div");
        paramEl.innerHTML = `
            <label for="${param}">${param}:</label>
            <input type="text" id="${param}" name="${param}" placeholed="Enter a value" stype=padding-left:4em>
            <br><br>
        `;
        
        return paramEl;
        
    };

    renderSubmit = () => {
        let submitEl = document.createElement("div");
        submitEl.innerHTML = `<input type="submit" value="Execute method">`;
        return submitEl;
    };

}