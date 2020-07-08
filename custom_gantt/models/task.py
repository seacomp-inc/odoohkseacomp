# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class Task(models.Model):
    _inherit = 'project.task'


    task_color = fields.Integer(compute="get_task_color",store=True)
    user_name = fields.Char(compute="get_task_user_name",store=True)

    @api.depends('x_studio_effective_completion_date')
    def get_task_color(self):
    	for rec in self:
    		rec.task_color = 0 if not rec.x_studio_effective_completion_date else 3

    @api.depends('user_id')
    def get_task_user_name(self):
    	for rec in self:
    		rec.user_name = rec.user_id.name
