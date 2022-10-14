import odoo.http as http

class TopResultController(http.Controller):

    @http.route('/get-data-predict', type='json',website=False, auth='public', methods=['POST'], csrf=False, cors="*")
    def get_predict(self, **arg):
        # print('------------------self----------------------', self)
        # flag = http.request.jsonrequest
        # print('============flag=======', flag)
        result = http.request.env['top.trend'].get_data_predict(arg)
     
        return result
      