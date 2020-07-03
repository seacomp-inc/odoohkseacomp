odoo.define('pos_multiple_uom.ProductUomButton', function (require) {
    "use strict";

    var ajax = require('web.ajax');
    var core = require('web.core');
    var qweb = core.qweb;
    var screens = require('point_of_sale.screens');
    var models = require('point_of_sale.models');

    ajax.loadXML('/pos_multiple_uom/static/src/xml/pos_multiple_uom_template.xml', qweb);

    models.load_models({
        model: 'x_product.multiple.uom',
        fields: ['x_uom_id','x_product_id','x_price', 'x_qty'],
        loaded: function(self, uom) {
            self.uom_price = {};
            var uom_vals = [];
            if(uom.length) {
                for (var i = 0; i < uom.length; i++) {
                    uom_vals.push({
                        product_id: uom[i].x_product_id[0],
                        uom_id: uom[i].x_uom_id,
                        qty: uom[i].x_qty,
                        price: uom[i].x_price,
                    });
                }
            self.uom_price = uom_vals
            }
        },
    });

    var _super_posModel = models.PosModel.prototype;
    models.PosModel = models.PosModel.extend({
        _save_to_server: function (orders, options) {
            if (orders.length > 0) {
                for (var i = 0; i < orders.length; i++) {
                    orders[i].data.lines.forEach(function (line) {
                        var product_uom = posmodel.uom_price.filter((p) => { return p.uom_id[0] == posmodel.db.get_product_by_id(line[2].product_id).uom_id[0] })[0]
                        var order_uom = posmodel.uom_price.filter((p) => { return p.uom_id[0] == line[2].uom_id })[0];
                        line[2].qty = (line[2].qty * product_uom.qty) / order_uom.qty;
                    });
                }
            }
            return _super_posModel._save_to_server.apply(this,arguments);
        }
    });

    var _super_orderline = models.Orderline.prototype;
    models.Orderline = models.Orderline.extend({
        initialize: function(attr, options) {
            _super_orderline.initialize.call(this, attr, options);
            if (options.json) {
                if (!this.uom_id){
                    this.uom_id = this.product.uom_id;
                    return;
                }
            }
            this.uom_id = options.product.uom_id;
        },

        get_unit: function(){
            if (this.uom_id) { 
                var unit_id = this.uom_id;
            }
            else {
                var unit_id = this.product.uom_id;
            }
            if(!unit_id) {
                return undefined;
            }
            unit_id = unit_id[0];
            if(!this.pos) {
                return undefined;
            }
            return this.pos.units_by_id[unit_id];
        },

        set_uom: function(uom_id){
            this.order.assert_editable();
            this.uom_id = uom_id;
            this.trigger('change',this);
        },

        export_as_JSON: function(){
            var json = _super_orderline.export_as_JSON.call(this);
            json.uom_id = this.uom_id[0];
            return json;
        },
    });

    var ProductUomButton = screens.ActionButtonWidget.extend({
        template: 'ProductUomButton',
        button_click: function() {
            var line = this.pos.get_order().get_selected_orderline();
            if (line) {
                var uom = []
                for (var i = 0; i < line.pos.uom_price.length; i++) {
                    if (line.pos.uom_price[i].product_id == line.product.product_tmpl_id) {
                        uom.push(line.pos.uom_price[i])
                    }
                }
                if (uom) {
                    var list = _.map(uom, function (uom_id) {
                        return {
                            label: line.pos.units_by_id[uom_id.uom_id[0]].display_name,
                            item: line.pos.units_by_id[uom_id.uom_id[0]],
                        };
                    });
                    this.gui.show_popup('selection',{
                        title: 'UOM',
                        list: list,
                        confirm: function (uom_id) {
                            uom = {0:line.pos.units_by_id[uom_id.id].id, 1:line.pos.units_by_id[uom_id.id].name};
                            line.set_uom(uom);
                            var price = line.pos.uom_price.filter((p) => { return p.uom_id[0] == uom_id.id })[0].price
                            line.set_unit_price(price);
                            line.price_manually_set = true;
                        },
                    });
                }
            }
        },
    });

    screens.define_action_button({
        'name': 'uom',
        'widget': ProductUomButton,
    });

});
