  var custom = 0;
  //<!--=============================================================================-->
     function generate_graph()
	{
		if (custom == 1)
		{}
		else
		{
		var query = generate_query();
		}
        //<!--submits the query to the sqvizler server-->
        sgvizler.ui.submitQuery();
	}
	
	function generate_query()	
	{ 
		//<!--variables that hold selected options-->
		var firstVariable_id = document.getElementById("id_var_1").value;
		var secondVariable_id = document.getElementById("id_var_2").value;
		var filter_text_box = document.getElementById("id_filter_box").value;
		var checkBox_value = document.getElementById("id_check_box").checked;
		var radioButton1 = document.getElementById("id_filter_opt_contains").checked;
		var radioButton2 = document.getElementById("id_filter_opt_exact").checked;
		var radioButton3 = document.getElementById("id_filter_opt_arithmatic").checked;
		
		//<!---set the radiobutton to a hidden text box for later useage-->
		if(radioButton1)
		{document.getElementById("id_radiobutton_option").value = 1;}
		else if(radioButton2)
		{document.getElementById("id_radiobutton_option").value = 2;}
		else if(radioButton3)
		{document.getElementById("id_radiobutton_option").value = 3;}


				
        var queryTextBox = new Array(); //<!--initialise an array of 40 empty string variables-->
		for (var i=0 ; i<=40 ; i++) 
        {
            queryTextBox[i] = "";
        }
        
        var j = 1; //<!--array index marker -->
       
       //<!--starts query creation-->
        queryTextBox[j] ="SELECT";
        j++;
                
        //<!--put first and second variables into select statement ((only if selected))-->
        if(firstVariable_id != "")
        {
	        queryTextBox[j] = " ("+"?" + firstVariable_id + " as ?" + firstVariable_id + ")";
	        j++;
        }
        if(secondVariable_id != "")
        {
        	queryTextBox[j] = " ("+"?" + secondVariable_id + " as ?" + secondVariable_id + ")";
        	j++;
        }
        if(checkBox_value) //<!--if checkBox is selected-->
        {queryTextBox[j] =" (count(distinct ?part as ?Number_of_participants)";}
        else
        {queryTextBox[j] = "";} 
        j++;
        queryTextBox[j] = "\n\nWHERE \n{\n"+
            "?site rdf:type austalk:RecordingSite .\n"+
            "?site rdfs:label ?recording_site .\n" +
            "?part rdf:type foaf:Person .\n" +
            "?part austalk:recording_site ?site .\n";
                        
        j++;
        
        //<!--array of variable options-->
        var variableOptions = new Array();
        var counter = 0;
        variableOptions[counter] = "name"; counter++;
        variableOptions[counter] = "id"; counter++;
        variableOptions[counter] = "birthYear"; counter++;
        variableOptions[counter] = "ageGroup"; counter++;
        variableOptions[counter] = "pob_town"; counter++;
        variableOptions[counter] = "pob_state"; counter++;
        variableOptions[counter] = "pob_country"; counter++;
        variableOptions[counter] = "postcode"; counter++;
        variableOptions[counter] = "suburb"; counter++;
        variableOptions[counter] = "gender"; counter++;
        variableOptions[counter] = "education_level"; counter++;
        variableOptions[counter] = "ses"; counter++;
        variableOptions[counter] = "professional_category"; counter++;
        variableOptions[counter] = "professional_occupation"; counter++;
        variableOptions[counter] = "cultural_heritage"; counter++;
        variableOptions[counter] = "recording_site"; counter++;
        variableOptions[counter] = "first_language"; counter++;
        variableOptions[counter] = "other_languages"; counter++;
        variableOptions[counter] = "hobbies_details"; counter++;
        variableOptions[counter] = "student_enrollment"; counter++;
        variableOptions[counter] = "student_course"; counter++;

        
        //<!--array of corresponding statements for the where section of the query-->
        var whereStatement = new Array();
        var counter = 0;
        whereStatement[counter] ="austalk:name ?name .\n"; counter++;
        whereStatement[counter] ="austalk:id ?id .\n"; counter++;
		whereStatement[counter] ="dbp:birthYear ?birthYear .\n"; counter++;
		whereStatement[counter] ="austalk:ageGroup ?ageGroup .\n"; counter++;
		whereStatement[counter] ="austalk:pob_town ?pob_town .\n"; counter++;
		whereStatement[counter] ="austalk:pob_state ?pob_state .\n"; counter++;
		whereStatement[counter] ="austalk:pob_country ?pob_country .\n"; counter++;
		whereStatement[counter] ="austalk:postcode ?postcode .\n"; counter++;
		whereStatement[counter] ="austalk:suburb ?suburb .\n"; counter++;
		whereStatement[counter] ="foaf:gender ?gender .\n"; counter++;
		whereStatement[counter] ="austalk:education_level ?education_level .\n"; counter++;
		whereStatement[counter] ="austalk:ses ?ses .\n"; counter++;
		whereStatement[counter] ="austalk:professional_category ?professional_category .\n"; counter++;
		whereStatement[counter] ="austalk:professional_occupation ?professional_occupation .\n"; counter++;
		whereStatement[counter] ="austalk:cultural_heritage ?cultural_heritage .\n"; counter++;
		whereStatement[counter] =""; counter++;
		whereStatement[counter] ="austalk:first_language ?first_language .\n"; counter++;
		whereStatement[counter] ="austalk:other_languages ?other_languages .\n"; counter++;
		whereStatement[counter] ="austalk:hobbies_details ?hobbies_details .\n"; counter++;
		whereStatement[counter] ="austalk:student_enrollment ?student_enrollment .\n"; counter++;
		whereStatement[counter] ="austalk:student_course ?student_course .\n"; counter++;		var numOfOptions =  counter-1; //<!--- **Keep this variable ACCURATE** -->
		
		//<!--takes the first variable and inputs the appropriate where statement-->
        for (var k=0 ; k<=numOfOptions ; k++)
        {
            if(firstVariable_id == variableOptions[k])
            {
            	if (firstVariable_id == "recording_site")
            	{}
            	else
            	{
	                queryTextBox[j] = "?part " + whereStatement[k];
	                j++;
            	}
            }
        }
        
        //<!--takes the second variable and inputs the appropriate where statement-->
        for (var m=0 ; m<=numOfOptions ; m++)
        {
            if(secondVariable_id == variableOptions[m])
            {
            	if (firstVariable_id == "recording_site")
            	{}
            	else
            	{
	                queryTextBox[j] = "?part " + whereStatement[m];
	                j++;
            	}
            }
        }
     
     	 //<!--filters the 1st variable by the contents of the filterBox-->
        length = filter_text_box.length
        if(length == 0) //<!--if filterBox is blank do nothing-->
        {;}
        else
        {
        	if(document.getElementById("id_radiobutton_option").value == 1) //<!--if contains text chosen-->
        	{
        		queryTextBox[j] = "\nFILTER" + " regex(" + "?" + firstVariable_id + ", " + "\"" 
	        		+ filter_text_box +"\"" + ", \"i\"" + ")";
        	}
        	else if(document.getElementById("id_radiobutton_option").value == 2) //<!--if exact option-->
        	{
        		queryTextBox[j] = "\nFILTER" + "(" + "?" + firstVariable_id + " = " + "\"" 
	        		+ filter_text_box +"\""+ ")";
        	}
        	else if(document.getElementById("id_radiobutton_option").value == 3) //<!--if arithmatic-->
        	{
	        	queryTextBox[j] = "\nFILTER" + "(" + "?" + firstVariable_id + filter_text_box + ")";
        	}
        	j++;

        }
     
        queryTextBox[j] = 
            "\n}\n" +
                "\nGROUP BY";
        j++;
                
        //<!--if checkBox selected-->
        if(checkBox_value == true)
        {queryTextBox[j] ="";}
        else
        {queryTextBox[j] = "";}
        j++;
        
        //<!--includes first and second variables in the group by clause ((if required))-->
        if(firstVariable_id != "")
        {
	        queryTextBox[j] = " ?" + firstVariable_id;
	        j++;
        }
         if(secondVariable_id != "")
        {
        	queryTextBox[j] = " ?" + secondVariable_id;
        	j++;
        }
        //<!--orders the results by the first variable (alphabetically)-->
        if(firstVariable_id != "")
        {
        	queryTextBox[j] = "\nORDER BY ?" + firstVariable_id;
        	j++;
        }
        
        //<!--concatenates the strings to form the query (stored in queryTextBox[0])-->
        for (var n=1 ; n<=j-1 ; n++)
        {
            queryTextBox[0] = queryTextBox[0] + queryTextBox[n];
        }
        
        //<!--puts the query into the textBox ("sgvzlr_cQuery)-->
        document.getElementById("sgvzlr_cQuery").value = queryTextBox[0];
        
        //<!--checks the previous line worked and prints the query to screen (for debugging only)-->
        var q = document.getElementById("sgvzlr_cQuery").value;
      // DEBUGGING
      // alert(q);
        
        return queryTextBox[0];
        	}
    
    
//<!--=============================================================================-->     	
	function retreiveData() 
	{
		//<!-- fancy complex function that extracts the values from the URL query so you can use them--> 
		function getQueryString() 
		{
	  		var result = {}, queryString = location.search.substring(1),
	      	re = /([^&=]+)=([^&]*)/g, m;
	
	  		while (m = re.exec(queryString)) 
	  		{
	   			result[decodeURIComponent(m[1])] = decodeURIComponent(m[2]);
 			}

  		return result;
		}

	//<!--set the variables to the values in the URL query-->
		var firstVariable_id = getQueryString()["var_1"];
		var secondVariable_id = getQueryString()["var_2"];
		var filter_text_box = getQueryString()["Filter"];
		var checkBox_value = getQueryString()["check_box"];
		var radioButton = getQueryString()["radiobutton_option"];
		
		
		if(typeof filter_text_box === 'undefined')
		{filter_text_box = "";}
		
		
 		//<!--set the form to match the variables-->
 		document.getElementById("id_var_1").value = firstVariable_id;
 		document.getElementById("id_var_2").value = secondVariable_id;
		document.getElementById("id_check_box").checked = checkBox_value;
		document.getElementById("id_filter_box").value = filter_text_box;
		if(radioButton == "1")
		{
			document.getElementById("id_filter_opt_contains").checked=true;
		}
		else if(radioButton == "2")
		{
			document.getElementById("id_filter_opt_exact").checked=true;
		}
		else if(radioButton == "3")
		{
			document.getElementById("id_filter_opt_arithmatic").checked=true;
		}

	}
	
//<!--=============================================================================-->
	function save_query()
	{
		var query = generate_query();
		mywindow=window.open('','','width=800,height=200');
    	
    	mywindow.document.write('\"' + query + '\"');
	}
	 
//<!--=============================================================================-->
	function save_graph_old()
    {   	
    	var query = generate_query();
    	

    	mywindow=window.open('','','width=800,height=450');
    	
    	mywindow.document.write('<!DOCTYPE html>\n<html lang="en"><head><title>Query</title>');
    	mywindow.document.write("\n<script type=\"text/javascript\" src=\"http://ajax.googleapis.com/ajax/libs/jquery/1.6.2/jquery.min.js\"></script>\n<script type=\"text/javascript\" src=\"https://www.google.com/jsapi\"></script>\n<script type=\"text/javascript\" id=\"sgvzlr_script\" src=\"http://sgvizler.googlecode.com/svn/release/0.5/sgvizler.js\"></script>\n<script type=\"text/javascript\">\n// CONFIGURATION Sgvizler 0.5: Set variables to fit your setup.\n// NB! Do not let the last item in a list end with a comma.\n\n//// Query settings. The defaults settings are listed.\nsgvizler.option.query = {\n// Default query.\n'query':'SELECT  ?inst (count(?part) as ?partcount)\\nWHERE {\\n ?site rdf:type austalk:RecordingSite .\\n ?site rdfs:label ?inst .\\n ?part rdf:type foaf:Person .\\n ?part austalk:recording_site ?site .\\n}\\ngroup by ?inst',\n'endpoint':'http://sesame.stevecassidy.net/openrdf-sesame/repositories/bigasc',\n'endpoint_output':'json',\n// Default chart type. \n'chart':                'gPieChart',\n// Default log level. Must be either 0, 1, or 2. \n'loglevel':1\n};\n\n//// Prefixes\n// Add convenient prefixes for your dataset. rdf, rdfs, xsd, owl\n// are already set.  Examples: \nsgvizler.option.namespace['dc'] = 'http://purl.org/dc/terms/';\nsgvizler.option.namespace['ausnc'] = 'http://ns.ausnc.org.au/schemas/ausnc_md_model/';\nsgvizler.option.namespace['olac'] = 'http://www.language-archives.org/OLAC/1.1/';\nsgvizler.option.namespace['ice'] = 'http://ns.ausnc.org.au/schemas/ice/';\nsgvizler.option.namespace['foaf'] = 'http://xmlns.com/foaf/0.1/';\nsgvizler.option.namespace['graf'] = 'http://www.xces.org/ns/GrAF/1.0/';\nsgvizler.option.namespace['austalk'] = 'http://ns.austalk.edu.au/';\nsgvizler.option.namespace['protocol'] = 'http://id.austalk.edu.au/protocol/';\nsgvizler.option.namespace['austalkd'] = 'http://data.austalk.edu.au/';\nsgvizler.option.namespace['dbpedia'] = 'http://dbpedia.org/ontology/';\nsgvizler.option.namespace['geo'] = 'http://www.w3.org/2003/01/geo/wgs84_pos#';\n\n//// Leave this as is. Ready, steady, GO!\n$(document).ready(sgvizler.go());\n</script>");
    	
		mywindow.document.write('\n</head><body>');
		mywindow.document.write('\n\n<div id="age_distribution"\ndata-sgvizler-query=\"');
		mywindow.document.write(query);
		mywindow.document.write('\"\ndata-sgvizler-chart="'+
								'gColumnChart'+
								'"\n' +
								'data-sgvizler-loglevel="0"\n' +
								'data-sgvizler-chart-options="title=Age Distribution"' +
								'\nstyle="width:800px; height:400px;"></div> ');
		mywindow.document.write('\n<p>Graphs generated by Sgvizler which visualizes the' + 
								' result of SPARQL SELECT queries using javascript' +
								' <br>and the Google Visualization API. For more ' +
								'information, see the <a href="http://code.google.com' +
								'/p/sgvizler/">Sgvizler</a> homepage. <br>(c)' +
								' 2011 Martin G. Skj&#230;veland.\n</p>');
		mywindow.document.write('</body></html>');
		mywindow.document.close();
		mywindow.generate_graph();
    	
    }
    
//<!--=============================================================================--> 
    function save_graph() 
	{		
		var firstVariable_id = document.getElementById("id_var_1").value;
		var secondVariable_id = document.getElementById("id_var_2").value;
		
	    var printWindow = window.open("", "Print", "status=no, toolbar=no, scrollbars=yes", "false" );
		$("link, style, script").each(function() {
		$(printWindow.document.head).append($(this).clone())
		});
	    
	    var part1 ="<h3>" + firstVariable_id;
	    var part2 = " vs. " + secondVariable_id + "</h3>";
	    var part3 = "</h3>"
		if (custom == 0)
		{
			if (secondVariable_id != "")
			{
				var toInsertHeader = part1 + part2;  
			}
			else
			{
				var toInsertHeader = part1 + part3;
			}
		}
		else 
		{
			var toInsertHeader = "";
		}
		var toInsert = $("div.chart").html();
		$(printWindow.document.body).append(toInsertHeader);
		$(printWindow.document.body).append(toInsert);
	}


 
//<!--=============================================================================--> 
function options_clone() 
{
  var options = $("#id_var_1 option");
  $("#id_var_2").html(options.clone());
}

	 
//<!--=============================================================================--> 
function changeDropdowns() 
{	
	graphType = document.getElementById("sgvzlr_optChart").value;
	
	if (graphType == "gPieChart" || graphType == "gColumnChart"|| graphType == "gBarChart")
	{
		document.getElementById('id_var_2').style.display='none';
	}
	else
	{
		document.getElementById('id_var_2').style.display='inline';
	}
}

//<!--=============================================================================--> 

function unhideTextbox()
{
	document.getElementById('sgvzlr_cQuery').style.display='block';	
	custom = 1;
}	
	