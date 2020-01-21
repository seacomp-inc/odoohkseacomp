odoo.define('mrr_jsi.mrp_bom_rediness_report', function (require) {
'use strict';

var core = require('web.core');
var framework = require('web.framework');
var stock_report_generic = require('stock.stock_report_generic');

var QWeb = core.qweb;
var _t = core._t;

var MrpBomReportJsi = stock_report_generic.extend({
    events: {
        'click .o_mrp_bom_unfoldable': '_onClickUnfold',
        'click .o_mrp_bom_foldable': '_onClickFold',
        'click .o_mrp_bom_action': '_onClickAction',
        'click .o_mrp_bom_action_open_pol_tree': '_onClickShowPOL',
    },
    get_html: function() {
        var self = this;
        var args = [
            this.given_context.active_id,
            this.given_context.searchQty || 1,
            this.given_context.searchVariant,
        ];
        return this._rpc({
                model: 'report.mrr_jsi.report_bom_material_rediness',
                method: 'get_html',
                args: args,
                context: this.given_context,
            })
            .then(function (result) {
                self.data = result;
            });
    },
    set_html: function() {
        var self = this;
        return this._super().then(function () {
            self.$el.html(self.data.lines);
            self.update_cp();
        });
    },
    render_html: function(event, $el, result){
        $el.after(result);
        $(event.currentTarget).toggleClass('o_mrp_bom_foldable o_mrp_bom_unfoldable fa-caret-right fa-caret-down');
    },
    get_bom: function(event) {
      var self = this;
      var $parent = $(event.currentTarget).closest('tr');
      var activeID = $parent.data('id');
      var productID = $parent.data('product_id');
      var lineID = $parent.data('line');
      var qty = $parent.data('qty');
      var level = $parent.data('level') || 0;
      return this._rpc({
              model: 'report.mrr_jsi.report_bom_material_rediness',
              method: 'get_bom',
              args: [
                  activeID,
                  productID,
                  parseFloat(qty),
                  lineID,
                  level + 1,
              ]
          })
          .then(function (result) {
              self.render_html(event, $parent, result);
          });
    },
    update_cp: function () {
        var status = {
            cp_content: {
                $buttons: this.$buttonPrint,
                $searchview_buttons: this.$searchView
            },
        };
        return this.update_control_panel(status);
    },
    _onClickUnfold: function (ev) {
        var redirect_function = $(ev.currentTarget).data('function');
        this[redirect_function](ev);
    },
    _onClickFold: function (ev) {
        this._removeLines($(ev.currentTarget).closest('tr'));
        $(ev.currentTarget).toggleClass('o_mrp_bom_foldable o_mrp_bom_unfoldable fa-caret-right fa-caret-down');
    },
    _onClickAction: function (ev) {
        ev.preventDefault();
        return this.do_action({
            type: 'ir.actions.act_window',
            res_model: $(ev.currentTarget).data('model'),
            res_id: $(ev.currentTarget).data('res-id'),
            views: [[false, 'form']],
            target: 'current'
        });
    },
    _onClickShowPOL: function (ev) {
        ev.preventDefault();
        var self = this
        var ids = $(ev.currentTarget).data('res-id');
        return self._rpc({
                    model: 'ir.model.data',
                    method: 'xmlid_to_res_id',
                    kwargs: {xmlid: 'mrr_jsi.purchase_order_line_tree_mrr_jsi'},
                }).then(function(view_id){
                    self.do_action({
                        name: _t('Purchase Order Lines'),
                        type: 'ir.actions.act_window',
                        res_model: $(ev.currentTarget).data('model'),
                        domain: [['id', 'in', ids]],
                        views: [[view_id, 'list']],
                        view_mode: 'list',
                        target: 'current',
                    });
                });
    },
    _reload: function () {
        var self = this;
        return this.get_html().then(function () {
            self.$el.html(self.data.lines);
        });
    },
    _removeLines: function ($el) {
        var self = this;
        var activeID = $el.data('id');
        _.each(this.$('tr[parent_id='+ activeID +']'), function (parent) {
            var $parent = self.$(parent);
            var $el = self.$('tr[parent_id='+ $parent.data('id') +']');
            if ($el.length) {
                self._removeLines($parent);
            }
            $parent.remove();
        });
    },
});

core.action_registry.add('mrp_bom_rediness_report', MrpBomReportJsi);
return MrpBomReportJsi;

});
