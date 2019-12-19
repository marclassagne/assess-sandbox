////////////////////////////////////////////////////////////////////////////////////////////////////////
///				OBJET ARBRE
////////////////////////////////////////////////////////////////////////////////////////////////////////

var Arbre = function(id, target, display_settings, assess_type) {
  this.questions_val_min=" ";
  this.questions_val_max=" ";
  this.questions_val_mean=" ";
  this.questions_proba_haut=" ";
  this.div_target = target;
  this.identifiant = id;
  this.displayed = false;
	this.type = display_settings;
  this.html = '<div class="proba_tree" style="text-align: center;" id=\"tree_' + this.identifiant + '\"></div>';
  this.assess_type = assess_type;
};

Arbre.prototype.display = function() {
  if (!this.displayed && this.div_target) {
    // we append the html
    $(this.div_target).append(this.html);
    this.displayed = true;
  }
};

Arbre.prototype.remove = function() {
  if (this.displayed) {
    $('#tree_' + this.identifiant).remove();
    this.displayed = false;
  }
};

Arbre.prototype.update = function() {
  if (this.type == "trees") {
    this.questions_val_min = this.questions_val_min.replace(/<br\/>/g,"\n");
    this.questions_val_max = this.questions_val_max.replace(/<br\/>/g,"\n");
    this.questions_val_mean = this.questions_val_mean.replace(/<br\/>/g,"\n");
    var _this = this
    var ajaxdata = {
      "type": "tree",
      "gain": this.questions_val_mean,
      "upper_label":this.questions_val_max,
      "bottom_label":this.questions_val_min,
      "upper_proba":this.questions_proba_haut,
      "bottom_proba":(1 - this.questions_proba_haut).toFixed(2),
      "assess_type":this.assess_type
    };
    $.post('ajax', JSON.stringify(ajaxdata), function(data) {
      $('#tree_' + _this.identifiant).empty();
      $('#tree_' + _this.identifiant).append("<img src='data:image/png;base64,"+ data +"' alt='tree' />");
    });
  } else {
      this.questions_val_min = this.questions_val_min.replace(/<br\/>/g,"\n");
      this.questions_val_max = this.questions_val_max.replace(/<br\/>/g,"\n");
      this.questions_val_mean = this.questions_val_mean.replace(/<br\/>/g,"\n");
		  var _this = this
      if (this.questions_val_mean != "") {
        var ajaxdata = {
          "type": "pie_chart",
          "names": [this.questions_val_mean, this.questions_val_min, this.questions_val_max],
          "probas": [this.questions_proba_haut, (1 - this.questions_proba_haut).toFixed(2)],
        };
        $.post('ajax', JSON.stringify(ajaxdata), function(data) {
    			$('#tree_' + _this.identifiant).empty();
    			$('#tree_' + _this.identifiant).append(data);
        });
      }
      else {
        var ajaxdata = {
          "type": "pie_chart",
          "names": [this.questions_val_min, this.questions_val_max],
          "probas": [this.questions_proba_haut, (1 - this.questions_proba_haut).toFixed(2)],
        };
        $.post('ajax', JSON.stringify(ajaxdata), function(data) {
    			$('#tree_' + _this.identifiant).empty();
    			$('#tree_' + _this.identifiant).append(data);
        });
      }

  }

};
