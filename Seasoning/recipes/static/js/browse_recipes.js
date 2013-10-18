/**
 * This function makes an ajax-post request to get an updated list of
 * recipes conforming to the users' search parameters
 * 
 * @param page
 * 	If present, the given page of results is shown
 * 	If not, the first page of results is shown
 */
function update_recipes(page) {
	var url;
	if (page) {
		url = "/recipes/?page=" + page;
	} else {
		url = "/recipes/";
	}

	$.ajax({
		type : "POST",
		url : url,
		data : $("form.keywords").serialize(),
		success : function(data) {
			// The url returns full html
			$("#recipe-summaries-wrapper").html(data);
		}
	});
	return false;
};

/**
 * This timer will be reset after the user has typed his last character
 * in the search field. This prevents a buttload of queries when a user is
 * search for a long string.
 */
var timer;

$(document).ready(function() {
	
	// Toggle the Advanced Search Window
	$("#advanced-link").click(function() {
		if ($("#advanced-search").is(":visible")) {
			// Hide
			$("#advanced-search").slideUp(1000, function() {
				$("#advanced-link").text("Geavanceerd Zoeken");
				$("#recipe-summaries-wrapper").css("width", "960px");
				$("#id_advanced_search").val("False");
				update_recipes();
			});
		} else {
			// Show
			$("#recipe-summaries-wrapper").css("width", "720px");
			$("#advanced-search").slideDown(1000);
			$("#advanced-link").text("Niet-geavanceerd zoeken");
			$("#id_advanced_search").val("True");
			update_recipes();
		}
		return false;
	});

	// Activate the buttons that change the order direction
	$(".order-arrow").click(function() {
		if (!$(this).hasClass("active")) {
			var active_order_arrow = $(".order-arrow.active");
			active_order_arrow.removeClass("active");
			$(this).addClass("active");
			if ($(this).hasClass("up")) {
				$("#id_sort_order_0").click();
			} else {
				$("#id_sort_order_1").click();
			}
		}
		update_recipes();
		return false;
	});

	// Activate the buttons for veganism selection
	$(".veg-choice").each(function() {
		if (!$(this).children("input").prop("checked")) {
			$(this).removeClass("active");
		}
		$(this).click(function() {
			if ($(this).hasClass("active")) {
				$(this).removeClass("active");
				$(this).children("input").prop('checked', false);
			} else {
				$(this).addClass("active");
				$(this).children("input").prop('checked', true);
			}
			update_recipes();
			return false;
		});
	});

	// Activate the button for the include ingredients operator
	$("#incl-ings .option").click(function() {
		if (!$(this).hasClass("active")) {
			var active_option = $("#incl-ings .option.active");
			active_option.removeClass("active");
			$(this).addClass("active");
			if ($(this).hasClass("and")) {
				$("#id_include_ingredients_operator_0").click();
			} else {
				$("#id_include_ingredients_operator_1").click();
			}
		}
		update_recipes();
		return false;
	});

	// Activate the input field for including ingredients
	$("#include-ingredients-input").pressEnter(function() {
		if ($(this).val() != "") {
			// If the user pressed enter while
			// in the input field, and it
			// contains text,
			// add another ingredient to the
			// filter
			var current_form_num = parseInt($("#id_include-TOTAL_FORMS").val());
			$("#id_include-TOTAL_FORMS").val(current_form_num + 1);
			var empty_form = $("#id_include-__prefix__-name");
			var new_form = empty_form.clone();
			new_form.attr("id", new_form.attr("id").replace("__prefix__", current_form_num));
			new_form.attr("name", new_form.attr("name").replace("__prefix__",current_form_num));
			new_form.val($(this).val());
			new_form.insertBefore(empty_form);
			// Display the new ingredient as
			// being in the filter
			var new_ing = $('<a href="#"><div class="filtered-ingredient">' + $(this).val() + '</div></a>');
			new_ing.click(function() {
				new_form.remove();
				$(this).remove();
				update_recipes();
				return false;
			});
			$("#included-ingredients").append(new_ing);
			$(this).val("");
			update_recipes();
		}
	});
	
	// Activate the input field for excluding ingredients
	$("#exclude-ingredients-input").pressEnter(function() {
		if ($(this).val() != "") {
			// If the user pressed enter while
			// in the input field, and it
			// contains text,
			// add another ingredient to the
			// filter
			var current_form_num = parseInt($("#id_exclude-TOTAL_FORMS").val());
			$("#id_exclude-TOTAL_FORMS").val(current_form_num + 1);
			var empty_form = $("#id_exclude-__prefix__-name");
			var new_form = empty_form.clone();
			new_form.attr("id", new_form.attr("id").replace("__prefix__",current_form_num));
			new_form.attr("name", new_form.attr("name").replace("__prefix__",current_form_num));
			new_form.val($(this).val());
			new_form.insertBefore(empty_form);
			// Display the new ingredient as
			// being in the filter
			var new_ing = $('<a href="#"><div class="filtered-ingredient">' + $(this).val() + '</div></a>')
			new_ing.click(function() {
				new_form.remove();
				$(this).remove();
				update_recipes();
				return false;
			});
			$("#excluded-ingredients").append(new_ing);
			$(this).val("");
			update_recipes();
		}
	});
	
	// Update recipe list on filter change
	$("#id_sort_field").change(update_recipes);
	$("input[name='cuisine']").change(update_recipes);
	$("input[name='course']").change(update_recipes);
	
	/**
	 * Update the recipe list when the user types a search query
	 * 
	 * If the user is typing multiple characters, we wait until he
	 * has finished typing (delay of 1s)
	 */
	// Start the timer when more than 3 chars have been typed
	$("#id_search_string").keyup(function() {
		if ($(this).val().length >= 3) {
			timer = setTimeout(update_recipes, 1000);
		}
	});
	// Stop the timer when a new char is being typed
	$("#id_search_string").keydown(function() {
		clearTimeout(timer);
	});
	
	// Force a search by pressing the Return key when typing a query
	$("#id_search_string").pressEnter(function() {
		update_recipes;
		// Stop the timer when a search is being forced
		timer = clearTimeout(timer);
	});
});