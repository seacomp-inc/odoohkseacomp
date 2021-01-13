odoo.define('supply_chain_report_jsi.stock.move.tree', function (require) {
"use strict";
    const ListController = require('web.ListController');
    const ListView = require('web.ListView');

    const viewRegistry = require('web.view_registry');

    function renderGenerateReportButton() {
        if (this.$buttons) {
            const self = this;
            this.$buttons.on('click', '.o_button_generate_report', function () {
                self.do_action('supply_chain_report_jsi.action_generate_report');
            });
        }
    }

    const SupplyChainReportListController = ListController.extend({
        init: function () {
            this._super.apply(this, arguments);
            this.buttons_template = 'SupplyChainReportListView.buttons';
        },
        renderButtons: function () {
            this._super.apply(this, arguments);
            renderGenerateReportButton.apply(this, arguments);
        }
    });

    const SupplyChainReportListView = ListView.extend({
        config: _.extend({}, ListView.prototype.config, {
            Controller: SupplyChainReportListController,
        }),
    });

    viewRegistry.add('view_move_tree_supplier_chain_report_jsi', SupplyChainReportListView);
});
