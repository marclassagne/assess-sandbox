%include('header_init.tpl', heading='Settings')
<div class="alert alert-success" role="alert" id="settings_modified" >
      The settings have been succesfully modified
</div>

<form id="settings">
    <div class="form-group">
        <label for="decimals_equations">Number of decimals in equations</label>
        <input type="number" min=0 step=1 class="form-control form-control-inline" id="decimals_equations" aria-describedby="decimals_equations_help" />
        <small id="decimals_equations_help" class="form-text text-muted">Type the number of decimals in displayed equations (default: 3)</small>
    </div>
    <div class="form-group">
        <label for="decimals_dpl">Number of decimals in DPL and Excel equations</label>
        <input type="number" min=0 step=1 class="form-control form-control-inline" id="decimals_dpl" aria-describedby="decimals_dpl_help" />
        <small id="decimals_dpl_help" class="form-text text-muted">Type the number of decimals displayed in DPL and Excel equations (default: 8)</small>
    </div>
    <div class="form-group">
        <label for="proba_ce">Probability of CE method</label>
        <input type="number" min=0 step=0.01 class="form-control form-control-inline" id="proba_ce" aria-describedby="proba_ce_help" />
        <small id="proba_ce_help" class="form-text text-muted">Type the probability used in the certainty equivalent method (default: 0.3)</small>
    </div>
    <div class="form-group">
        <label for="proba_le">Probability of LE method</label>
        <input type="number" min=0 step=0.01 class="form-control form-control-inline" id="proba_le" aria-describedby="proba_le_help" />
        <small id="proba_le_help" class="form-text text-muted">Type the probability used in the lottery equivalents method (default: 0.3)</small>
    </div>
    <div class="form-group">
        <p><strong>Select the language used in Excel export and displayed equations (default: english)</strong></p>
        <label class="form-check-inline"><input type="radio" class="form-check-input" name="language" id="english" value="english"> English</label>
        <label class="form-check-inline"><input type="radio" class="form-check-input" name="language" id="french" value="french"> French</label>
    </div>
    <div class="form-group">
        <p><strong>Select the type of display for assessements (default: trees)</strong></p>
        <label class="form-check-inline"><input type="radio" class="form-check-input" name="display" id="trees" value="trees"> Trees</label>
        <label class="form-check-inline"><input type="radio" class="form-check-input" name="display" id="pie_charts" value="pie_charts"> Pie charts</label>
    </div>
    <button type="submit" class="btn btn-primary">Submit</button>
</form>

<br />


%include('header_end.tpl')
%include('js.tpl')

<script>
    $(function() {
        $("#settings_modified").hide();
		$('li.settings').addClass("active");

        var assess_session = JSON.parse(localStorage.getItem("assess_session"));

        if (!assess_session) {
            assess_session = {
                "attributes": [],
                "k_calculus": [{
                    "method": "multiplicative",
                    "active": "false",
                    "k": [],
                    "GK": null,
                    "GU": null
                }, {
                    "method": "multilinear",
                    "active": "false",
                    "k": [],
                    "GK": null,
                    "GU": null
                }],
                "settings": {
                    "decimals_equations": 3,
                    "decimals_dpl": 8,
                    "proba_ce": 0.3,
                    "proba_le": 0.3,
                    "language": "english",
                    "display": "trees"
                }
            };
            localStorage.setItem("assess_session", JSON.stringify(assess_session));
        }

        var settings = assess_session.settings;

        $("#decimals_equations").val(settings.decimals_equations);
        $("#decimals_dpl").val(settings.decimals_dpl);
        $("#proba_ce").val(settings.proba_ce);
        $("#proba_le").val(settings.proba_le);
        $("#" + settings.language).prop("checked", true);
        $("#" + settings.display).prop("checked", true);


        $("#settings").submit(function(e) {
            e.preventDefault();
            settings.decimals_equations = $("#decimals_equations").val();
            settings.decimals_dpl = $("#decimals_dpl").val();
            settings.proba_ce = $("#proba_ce").val();
            settings.proba_le = $("#proba_le").val();
            var language = $("input[type='radio'][name='language']:checked");
            settings.language = language.val();
            var display = $("input[type='radio'][name='display']:checked");
            settings.display = display.val();
            localStorage.setItem("assess_session", JSON.stringify(assess_session));
            $("#settings_modified").fadeIn();
        });
    });
</script>
