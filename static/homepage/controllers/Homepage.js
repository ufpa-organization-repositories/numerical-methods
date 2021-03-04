class Homepage{

	constructor(){
		console.log('initialize');
		this.formEl = document.querySelector("#chapters");
		this.initialize();		
	}

	initialize(){
		this.getChapters();
	}

	addChapterEl(obj) {
		obj.chapters.forEach((chapter, index) => {			
			let chapterEl = this.renderChapterButton(chapter);
			this.formEl.appendChild(chapterEl);
			console.log(chapterEl);
		});
	}

	getChapters(){
		const url = 'chapters'
			fetch(url)
				.then(resp => resp.json())
				.then(obj => {
					console.log(obj);
					this.addChapterEl(obj);
					})
	}

	renderChapterButton = (chapter) => {
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
		chapterEl.innerHTML = `<button class="button-elem" type="submit" value="${chapter}" name="chapter">${chapter}</button>`;
		return chapterEl;

	}
}