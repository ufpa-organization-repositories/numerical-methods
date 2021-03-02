class Method {

    constructor () {
        this.logTableEl = document.querySelector(".table");
        this.graphEl = document.querySelector(".graphs");
        this.initialize();
    }

    initialize(){
        // this.getGraphs();
        this.getGraphs2();
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

    // works, too. I am using fetch to learn new way of doing async request
    getGraphs(){
        this.httpGetAsync('http://127.0.0.1:5000/graphs', (response) => {
            let obj = JSON.parse(response);
            console.log(obj);
            obj.graphs.forEach( (graph, index) => {
                console.log(index, graph);
            })
        })
    }

    getGraphs2(){
        const url = 'graphs'
            fetch(url)
                .then(resp => resp.json())
                .then(obj => {
                    // const itens = estados.reduce(
                    //     (html, estado) => html + `<li>${estado.nome}</li>`, ''
                    // )
                    // document.body.insertAdjacentHTML('beforeend', `<ul>${itens}</ul>`)                    
                    console.log(obj);

                    // display graphEl if there's graphs
                    console.log('length: ', obj.graphs.length);
                    if (obj.graphs.length > 0 ) {
                        this.graphEl.style.display = "block";
                    }

                    obj.graphs.forEach(graph => {
                        let graphEl = this.renderGraph(graph);
                        this.graphEl.appendChild(graphEl);
                    });
                })

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

    renderGraph = (graph) => {
        let graphEl = document.createElement("div");
        graphEl.innerHTML = `<img src="data:image/gif;base64,${graph}">`;
        return graphEl;
    }        

}