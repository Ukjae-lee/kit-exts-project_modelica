import omni.ext
import omni.ui as ui
import requests
import json

class SimulationExtension(omni.ext.IExt):
    def on_startup(self, ext_id):
        self._window = ui.Window("Simulation Parameters", width=300, height=300)
        with self._window.frame:
            with ui.VStack():
                # x_var_init 입력
                ui.Label("x_var_init:")
                self.x_var_init_model = ui.SimpleIntModel()
                self.x_var_init_field = ui.IntField(model=self.x_var_init_model)

                # x_delta 입력
                ui.Label("x_delta:")
                self.x_delta_model = ui.SimpleFloatModel()
                self.x_delta_field = ui.FloatField(model=self.x_delta_model)

                # 전송 버튼
                ui.Button("Submit", clicked_fn=self.submit_parameters)
                
                # 결과 표시 레이블
                self.result_label = ui.Label("", style={"color": "white"})
                
                # 결과 표시를 위한 스크롤 가능한 텍스트 영역
                with ui.ScrollingFrame(height=200):
                    self.result_text = ui.Label("", style={"color": "white"})

    def submit_parameters(self):
        # 사용자 입력 받기
        x_var_init = self.x_var_init_model.get_value_as_int()
        x_delta = self.x_delta_model.get_value_as_float()

        # FastAPI 서버로 시뮬레이션 요청 보내기
        simulation_data = {"x_var_init": x_var_init, "x_delta": x_delta}
        response = requests.post("http://127.0.0.1:8000/simulate/", json=simulation_data)
        
        # 결과 처리
        if response.status_code == 200:
            simulation_results = response.json()
            # 결과를 스크롤 가능한 텍스트 영역에 표시
            self.result_text.text = self.format_result_text(simulation_results.get('x_var_out', 'No result'))
        else:
            self.result_text.text = f"Error during simulation: {response.status_code}"

    def format_result_text(self, result_list):
        # 결과값을 줄 바꿈하여 표시하기 위한 함수
        result_str = json.dumps(result_list)
        wrapped_text = ""
        wrap_length = 50  # 한 줄에 표시할 문자 수
        
        # 주어진 길이로 텍스트를 줄 바꿈
        for i in range(0, len(result_str), wrap_length):
            wrapped_text += result_str[i:i+wrap_length] + "\n"
            
        return wrapped_text.strip()

EXTENSION = SimulationExtension()