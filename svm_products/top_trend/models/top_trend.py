from odoo import fields, models, api

from sklearn.svm import SVC
from sklearn.model_selection import train_test_split
import pandas as pd
from sklearn.metrics import accuracy_score 

class TopTrend(models.Model):
    _name = 'top.trend'
    _description = 'Description'
    _rec_name = 'name'

    name = fields.Char(string="Tên sản phẩm")
    link = fields.Char(string="Link sản phẩm")
    price = fields.Integer(string="Giá")
    out_stock_month = fields.Integer(string="Đã bán trong tháng")
    out_stock = fields.Integer(string="Tổng đã bán")
    type = fields.Char(string="Ngành hàng")
    seen = fields.Integer(string="Lượt xem")
    like = fields.Integer(string="Yêu thích")

    data_predict_trans = []

    #received data
    def get_data_predict(self, arg):

        self.data_predict_trans.clear()

        data_recei = arg.get('data_predict')

        list_id_predict = self.data_predict_trans
        for i in data_recei:
            list_id_predict.append(i)
        print(list_id_predict)
        print(len(list_id_predict))

    def train_data(self):
        # use data chose to train svm
        selected_ids_train = self.env.context.get('active_ids', [])
        selected_records_train = self.env['top.trend'].browse(selected_ids_train)

        out_month_svm =[]
        seen_svm =[]
        like_svm =[]
        data = {}
        df = pd.DataFrame(data)

        for item in selected_records_train:
            
            out_month_svm.append(item.out_stock_month)
            seen_svm.append(item.seen)
            like_svm.append(item.like)

        df['out_month_svm'] = out_month_svm
        df['seen_svm'] = seen_svm
        df['like_svm'] = like_svm

        X = df[:][["out_month_svm","seen_svm"]]
        y = df[:]["like_svm"]

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25)

        classifier = SVC(kernel='rbf')
        classifier.fit(X_train,y_train)
        y_pred = classifier.predict(X_test)

        score = "Predict (%.2f %% correct)" %(100*accuracy_score(y_test, y_pred))
        
        #trans data from result and predict
        out_to_predict = []
        seen_to_predict = []

        data_to_trans = {}
        df_to_trans = pd.DataFrame(data_to_trans)

        data_to_predict = self.data_predict_trans
        selected_records_predict = self.env['top.result'].browse(data_to_predict)

        for id_trans in selected_records_predict:
            out_to_predict.append(id_trans.out_stock_month)
            seen_to_predict.append(id_trans.seen)

        df_to_trans['out_to_predict'] = out_to_predict
        df_to_trans['seen_to_predict'] = seen_to_predict

        X_to_predict = df_to_trans[:][["out_to_predict","seen_to_predict"]]

        y_finally = classifier.predict(X_to_predict)

        #print result
        a = len(y_finally)
        i = 0
        for paste in selected_records_predict:
            if i < a :
                paste.like = y_finally[i]
                i += 1

        #trans view and result
        tree_view_id = self.env.ref("top_trend.top_result_tree_view").id
        form_view_id = self.env.ref("top_trend.top_result_form_view").id

        return {
            'type': 'ir.actions.act_window',
            'name': score,   
            'res_model': 'top.result',
            'views': [(tree_view_id, 'tree'),(form_view_id, 'form')],
            'target': 'current',
            'flags': {'search_view': True, 'action_buttons': True},
        }
    
    