window.onload = function(){
	addEventClick("terms");

	var searchTerm = document.getElementById("searchTerm");
	var searchInput = document.getElementById("search");
	var searchLabel = document.getElementById("searchLabel");

	var spinner = document.getElementById("spinner");
	
	var arrowLeft = document.getElementById("arrowLeft");
	var arrowReight = document.getElementById("arrowRight");
	var chipAlert = document.getElementById("chip-alert");
	var switchButton = document.getElementById("switch");

	var definitionDiv = document.getElementById("definitionDiv");
	var definitionTab = document.getElementById("definition-tab");
	
	var relations = [];
	var sizeRel =  0;

	arrowLeft.onclick = function(){
		getTermsByRelation("left");
	};
	
	arrowReight.onclick = function(){
		getTermsByRelation("right");
	};

	//searchInput.onkeyup = function(){
	$("#search").on('input', function(){
	// console.log(searchInput.value);
		var dataList = document.getElementById('datalist');
		$("#datalist").empty();
		var options;
		$.getJSON($SCRIPT_ROOT + "auto_completion", {
				mot: JSON.stringify(searchInput.value)
			},
			function(data){
	 			data.result.forEach(function(item){					
					var option = document.createElement('option');
				    option.value = item[0].replace("\\", "");
				    dataList.appendChild(option);
				});
		$("#search").focus();
		
		});
		//$("#search").click();
		$("#search").focus();
		
	});

	searchTerm.onclick = function(){
		var term = searchInput.value;//.toLowerCase();
		//console.log("switchButton " + switchButton.checked);

		spinner.style.display ="";
		spinner.className += " is-active";
		chipAlert.style.display ="none";

		var searchRes = document.getElementById("searchRes");
		searchRes.innerHTML = "";

		arrowReight.style.display = "none";
		arrowLeft.style.display = "none";

		definitionDiv.style = 'display:none';
		definitionTab.innerHTML = "";


		if(switchButton.checked){

			$.getJSON($SCRIPT_ROOT + "expression", {
				expression: JSON.stringify(term)
			},
			function(data){
				if(data.error){
					spinner.className ="mdl-spinner mdl-js-spinner";
					chipAlert.style.display = "";
					console.log(data.error);

				}else if(data.result.length != 0){
					spinner.className ="mdl-spinner mdl-js-spinner";
					spinner.style.display ="none";
				
					var text = "";
					data.result.forEach(function(term, i){
						text += "<a class='terms' href='#' title= 'Poids:"+ term[1] +"'>" + term[0] + "</a>  ";
					});
					searchRes.innerHTML = "<b class='noeud'>"+ term.toUpperCase() +"</b><br><br> "+ text;
					addEventClick("terms");

				}else{

					arrowReight.style.display = "none";
					arrowLeft.style.display = "none";
					chipAlert.style.display ="none";

				}
			});

		//});
	} else {

		$.getJSON($SCRIPT_ROOT + "noeud/info", {
			noeud: JSON.stringify(term)
		},
		function(data){
					//console.log(data);
					/*
					if(data.error){
						spinner.className ="mdl-spinner mdl-js-spinner";
						chipAlert.style.display = "";
						console.log(data.error);


					} else 
					*/
					if( data.definition.length > 0){
						definitionDiv.style = 'display:';
						definitionTab.innerHTML = "<p class=''>"+data.definition + "</p>";
						
					}
				});

		$.getJSON($SCRIPT_ROOT + "sortant", {
			noeud: JSON.stringify(term)
		}, function(data){
				//console.log(data);
				if(data.error){
					spinner.className ="mdl-spinner mdl-js-spinner";
					chipAlert.style.display = "";
					console.log(data.error);

				}
				else{
					relations = Object.keys(data.relations);
					sizeRel = relations.length;

					updateTabRelation(data);
					arrowReight.style.display = "flex";
					arrowLeft.style.display = "flex";
					
					spinner.className ="mdl-spinner mdl-js-spinner";
					spinner.style.display ="none";
					////console.log(data);
					if(sizeRel > 0 ){
						getNoeudRelationSortante(term, relations[0]);
					}
				}

			});

		}
	};

function getNoeudRelationSortante(term, relation){
		////console.log("relation " + relation);
		$.getJSON($SCRIPT_ROOT + "noeud/relationSortante", {
			noeud: JSON.stringify(term),
			relation: JSON.stringify(relation)
		}, function(data){
					////console.log(data);
					if(data.result.length != 0){
						var text = "";
						data.result.forEach(function(term, i){
							text += "<a class='terms' href='#' title= 'Poids:"+ term[1] +"'>" + term[0] + "</a>  ";
						});
						searchRes.innerHTML = "<b class='noeud'>"+ term.toUpperCase() +"</b>	<i class='name-relation'>" + relation + "</i><br><br> "+ text;
						addEventClick("terms");

					}else{

						arrowReight.style.display = "none";
						arrowLeft.style.display = "none";
						chipAlert.style.display ="none";

					}
					spinner.className ="mdl-spinner mdl-js-spinner";
					spinner.style.display ="none";

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
		////console.log(id + " " + th);
		if(th != null)
			th.parentNode.className = "is-selected";
		
	}

	function updateTabRelation(data) {
		var div = $('#tabRelations');
		div.empty();

		div.html("<table class='mdl-data-table mdl-js-data-table mdl-data-table--selectable mdl-shadow--2dp' >"+
						//"<thead><tr><th class='mdl-data-table__cell--non-numeric'>Relation</th></tr></thead>"+
						"<tbody id='tbody'></tbody></table>");
		var tbody = $('#tbody');
		
		var keys = Object.keys(data.relations);

		var relMobile = $('#relations-mobile');
		relMobile.empty();
		//console.log(relMobile);
		$('#relations-mobile').addClass("mdl-navigation");

		keys.forEach(function(d,i) {
			var relInfo = data.relations[d].replace("\"","\'");
			relMobile.append("<a class='mdl-navigation__link relations'  id='rm" + i + "' title='"+relInfo + "' href='#'>"+d+"</a>");
			var tr = $('<tr/>').appendTo(tbody);

			tr.append("<td class='mdl-data-table__cell--non-numeric relations' title=\""+relInfo+ "\" id='r" + i + "'>" + d + "</td>" );
			div.append("<div class='mdl-tooltip' data-mdl-for='r"	+ i + "'>" + data.relations[d] +"</div>" );
		});


		selectedRel(0);
		addEventClick("relations");

	}

	var idRel = 0; 
	function getTermsByRelation(relation){
		//var sizeRel =  objLength(relations);
		////console.log("sizeRel " + sizeRel);
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
			//console.log("idRel " + relation);
		}
		if(idRel == sizeRel){
			idRel = 0;
			relation = relations[idRel];
		}
		
		idRel = relations.indexOf(relation);
		////console.log( idRel + " relation " + relation.replace(" ","") + " " +   typeof(Array.prototype.slice.call(relations)));
		
		selectedRel(idRel);

		var term = document.getElementById("search").value;
		
		searchRes.innerHTML ="<b>"+ term +"</b>	<i>" + relation + "</i><br>";
		spinner.className += " is-active";
		spinner.style.display ="";
		getNoeudRelationSortante(term, relation);
		/*
		$.getJSON($SCRIPT_ROOT + "relation_term", {
					term: JSON.stringify(term), 
					relation: JSON.stringify(relation)
				}, function(data){
					//console.log(data.result);
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
		//console.log(size)
		updateElem.forEach(function (element){
			if(elem == "terms"){
				element.addEventListener("click", function (){
					//console.log("terms "+ element.innerHTML);
					searchLabel.innerHTML = "";
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