from odoo import fields, models, api
import requests
import os
import pandas as pd


class TopResult(models.Model):
    _name = 'top.result'
    _description = 'Description'
    _rec_name = 'name'

    name = fields.Char(string="Tên sản phẩm")
    link = fields.Char(string="Link sản phẩm")
    price = fields.Integer(string="Giá")
    out_stock_month = fields.Integer(string="Đã bán trong tháng")
    out_stock = fields.Integer(string="Tổng đã bán")
    type = fields.Char(string="Ngành hàng")
    seen = fields.Integer(string="Lượt xem")
    like = fields.Char(string="Dự đoán yêu thích")

    # result_id = fields.Many2one('top.result') 

    def top_result(self):
        selected_ids = self.env.context.get('active_ids', [])
        selected_records = self.env['top.result'].browse(selected_ids)

        id_trans = []

        for item in selected_records:
            id_trans.append(item.id)
    
        payload= {
            "params":{
                "data_predict" : id_trans
            }
        }

        response = requests.post('http://localhost:8079/get-data-predict', json=payload)

        tree_view_id = self.env.ref("top_trend.top_trend_tree_view").id
        form_view_id = self.env.ref("top_trend.top_trend_form_view").id

        return {
            'type': 'ir.actions.act_window',
            'name': 'Train Data',   
            'res_model': 'top.trend',
            'views': [(tree_view_id, 'tree'),(form_view_id, 'form')],
            'target': 'current',
            'flags': {'search_view': True, 'action_buttons': True},
        }
        
    