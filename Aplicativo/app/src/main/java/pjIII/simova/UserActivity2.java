package pjIII.simova;

import androidx.appcompat.app.AppCompatActivity;

import android.content.Intent;
import android.os.AsyncTask;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.TextView;
import android.widget.Toast;

public class UserActivity2 extends AppCompatActivity {

    private TextView atual;
    private TextView textView;
    private TextView evento1;
    private TextView data1;
    private TextView evento2;
    private TextView data2;
    private TextView evento3;
    private TextView data3;
    private TextView evento4;
    private TextView data4;
    private TextView evento5;
    private TextView data5;
    private String baseUrl;
    private String um = "Vaga livre e autenticada";
    private String dois = "Vaga livre, porém não autenticada";
    private String tres = "Vaga ocupada e autenticada";
    private String quatro = "Vaga ocupada, porém não autenticada";
    private Button pVaga;
    private Button aVaga;


    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_user2);
        baseUrl = "http://".concat(MainActivity.ip);
        baseUrl = baseUrl.concat(":5000/vaga/" +User.getVaga(5)+"/eventos");

        atual = (TextView) findViewById(R.id.t12);
        textView = (TextView) findViewById(R.id.textView9);
        textView.setText(textView.getText()+ User.getVaga(3));
        try {

            ApiAuthenticationClient apiAuthenticationClient =
                    new ApiAuthenticationClient(
                            baseUrl
                            , ""
                            , ""
                            ,"GET"
                    );

            AsyncTask<Void, Void, String> ex = new UserActivity2.NetworkOperation(apiAuthenticationClient);
            ex.execute();
        } catch (Exception ex) {
        }
        aVaga = (Button) findViewById(R.id.bt03);
        aVaga.setOnClickListener(new View.OnClickListener(){
            @Override
            public void onClick(View v) {
                goToUserActivity();
            }

        });
    }

    private void statusAtual() {
        if(User.getEventos(2).equals("1")){
            atual.setText(um);
        }
        else if (User.getEventos(2).equals("2")){
            atual.setText(dois);
        }
        else if (User.getEventos(2).equals("3")){
            atual.setText(tres);
        }else
            atual.setText(quatro);
    }

    private void goToUserActivity() {
        Intent intent = new Intent(this, UserActivity.class);
        startActivity(intent);
    }

    private void setEventos(){
        evento1 = (TextView) findViewById(R.id.t81);
        data1 = (TextView) findViewById(R.id.t51);
        if(User.eventos.size() >= 3 ){
            evento1.setText(User.getEventos(1));
            data1.setText(User.getEventos(0));
            statusAtual();
        }else{
            evento1.setText(null);
            data1.setText(null);
        }

        evento2 = (TextView) findViewById(R.id.t6);
        data2 = (TextView) findViewById(R.id.t61);
        if(User.eventos.size() >= 6 ){
            evento2.setText(User.getEventos(4));
            data2.setText(User.getEventos(3));
        }else {
            evento2.setText(null);
            data2.setText(null);
        }

        evento3 = (TextView) findViewById(R.id.t7);
        data3 = (TextView) findViewById(R.id.t71);
        if(User.eventos.size() >= 9 ){
            evento3.setText(User.getEventos(7));
            data3.setText(User.getEventos(6));
        }else {
            evento3.setText(null);
            data3.setText(null);
        }

        evento4 = (TextView) findViewById(R.id.t8);
        data4 = (TextView) findViewById(R.id.t81);
        if(User.eventos.size() >= 12 ){
            evento4.setText(User.getEventos(10));
            data4.setText(User.getEventos(9));
        }else{
            evento4.setText(null);
            data4.setText(null);
        }

        evento5 = (TextView) findViewById(R.id.t10);
        data5 = (TextView) findViewById(R.id.t101);
        if(User.eventos.size() >= 15 ){
            evento5.setText(User.getEventos(13));
            data5.setText(User.getEventos(12));
        }else{
            evento5.setText(null);
            data5.setText(null);
        }
    }

    public class NetworkOperation extends AsyncTask<Void, Void, String> {

        private ApiAuthenticationClient apiAuthenticationClient;
        private String isValidCredentials;

        /**
         * Overload the constructor to pass objects to this class.
         */
        public NetworkOperation(ApiAuthenticationClient apiAuthenticationClient) {
            this.apiAuthenticationClient = apiAuthenticationClient;
        }

        @Override
        protected String doInBackground(Void... params) {
            try {
                isValidCredentials = apiAuthenticationClient.ex();
            } catch (Exception e) {
                e.printStackTrace();
            }

            return null;
        }

        @Override
        protected void onPostExecute(String result){
            super.onPostExecute(result);
            if (isValidCredentials == "true"){
                setEventos();
                //Toast.makeText(getApplicationContext(), "Eventos atualizados" , Toast.LENGTH_SHORT).show();
            }else {// Login Failure
                Toast.makeText(getApplicationContext(), "Erro", Toast.LENGTH_LONG).show();
            }
        }
    }
}

