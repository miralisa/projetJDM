window.onload = function(){

	var searchTerm = document.getElementById("searchTerm");
	var spinner = document.getElementById("spinner");
	
	var arrowLeft = document.getElementById("arrowLeft");
	var arrowReight = document.getElementById("arrowRight");
	var chipAlert = document.getElementById("chip-alert");

	var relations = [];
	var sizeRel =  0;
		
	arrowLeft.onclick = function(){
		getTermsByRelation("left");
	};
	
	arrowReight.onclick = function(){
		getTermsByRelation("right");
	};
	
	searchTerm.onclick = function(){
		//console.log(term);
		var term = document.getElementById("search").value;//.toLowerCase();
		spinner.className += " is-active";
		chipAlert.style.display ="none";

		var searchRes = document.getElementById("searchRes");
		searchRes.innerHTML = "";

		$.getJSON($SCRIPT_ROOT + "sortant", {
				noeud: JSON.stringify(term)
			}, function(data){
				relations = Object.keys(data.relations);
				sizeRel = relations.length;

				updateTabRelation(data);
				addEventClick("terms");
				arrowReight.style.display = "flex";
				arrowLeft.style.display = "flex";
				
				spinner.className ="mdl-spinner mdl-js-spinner";
		
				//console.log(data);
				if(sizeRel > 0 ){
				getNoeudRelationSortante(term, relations[0]);
				}
						
			});
	};

	function getNoeudRelationSortante(term, relation){
		//console.log("relation " + relation);
		$.getJSON($SCRIPT_ROOT + "noeud/relationSortante", {
					noeud: JSON.stringify(term),
					relation: JSON.stringify(relation)
				}, function(data){
					console.log(data);
					if(data.result.length != 0){
					var text = "";
					data.result.forEach(function(term){
						text += "<a class='terms' href='#'>" + term[0] + "<a>  " + term[1] + ", ";
					});
					searchRes.innerHTML = "<b>"+ term +"</b>	<i>" + relation + "</i><br> "+ text;
			
					}else{

					arrowReight.style.display = "none";
					arrowLeft.style.display = "none";
					chipAlert.style.display ="flex";
			
					}
					spinner.className ="mdl-spinner mdl-js-spinner";
					

				});
	}

	function objLength(obj){
	  var i=0;
	  for (var x in obj){
	    if(obj.hasOwnProperty(x)){
	      i++;
	    }
	  } 
	  return i;
	}

	function selectedRel(id){
		//tr class="is-selected
		var tdRelations = [].slice.call(document.getElementsByClassName("relations"));
		tdRelations.forEach(function (element){
			element.parentNode.className = "";
		});
		var th = document.getElementById('r'+id);
		//console.log(th);
		//th.parentNode.className = "is-selected";
		
	}

	function updateTabRelation(data) {
		var div = $('#tabRelations');
		div.empty();

		div.html("<table class='mdl-data-table mdl-js-data-table mdl-data-table--selectable mdl-shadow--2dp' >"+
						"<thead><tr><th class='mdl-data-table__cell--non-numeric'>Relation</th></tr></thead>"+
						"<tbody id='tbody'></tbody></table>");
		var tbody = $('#tbody');
		
		var keys = Object.keys(data.relations);
			
		keys.forEach(function(d,i) {
			var tr = $('<tr/>').appendTo(tbody);
			tr.append("<td class='mdl-data-table__cell--non-numeric relations' id='r" + i + "'>" + d + "</td>");
             
		});
		selectedRel(0);
		addEventClick("relations");
	
	}

	var idRel = 0; 
	function getTermsByRelation(relation){
		//var sizeRel =  objLength(relations);
		//console.log("sizeRel " + sizeRel);
		if(relation == "right" ){//&& idRel < relations.lenght
			relation = relations[++idRel];
		} else /*if (relation == "right" && idRel == relations.lenght ){
			idRel = 1;
			relation = relations[idRel];
	
		}*/
		 if (relation == "left" && idRel != 0){
			relation = relations[--idRel];

		}else if (relation == "left" && idRel == 0){
			idRel = sizeRel-1;
			relation = relations[idRel];
			console.log("idRel " + relation);
		}
		if(idRel == sizeRel){
			idRel = 0;
			relation = relations[idRel];
		}
		
		idRel = relations.indexOf(relation);
		selectedRel(idRel);
	
		var term = document.getElementById("search").value;
		
		searchRes.innerHTML ="<b>"+ term +"</b>	<i>" + relation + "</i><br>";
		spinner.className += " is-active";
		getNoeudRelationSortante(term, relation);
		/*
		$.getJSON($SCRIPT_ROOT + "relation_term", {
					term: JSON.stringify(term), 
					relation: JSON.stringify(relation)
				}, function(data){
					console.log(data.result);
					if(data.result.length != 0){
						var text = "";
						data.result.forEach(function(child){
							text+="<a class='terms' href='#'>" + child + "<a>,		";
						});
						
						searchRes.innerHTML += text;
						//updateTabRelation(data.relations);
						addEventClick("terms");
					} else {

					}
					spinner.className ="mdl-spinner mdl-js-spinner";
					
				});
		*/
	}

	function addEventClick(elem){
		var updateElem = [].slice.call(document.getElementsByClassName(elem));
		var size = updateElem.length;
		console.log(size)
		updateElem.forEach(function (element){
			if(elem == "terms"){
				element.addEventListener("click", function (){
					//console.log("terms "+ element.innerHTML);
					var term = element.innerHTML;
					document.getElementById("search").value = term;
					searchTerm.click();

				});
			}else if(elem == "relations"){
				element.addEventListener("click", function (){
					//console.log("relations "+ element.innerHTML);
					var relation = element.innerHTML;
					getTermsByRelation(relation);
				});
			}
		});
	};



};