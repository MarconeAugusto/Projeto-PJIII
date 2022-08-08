package pjIII.simova;

import androidx.appcompat.app.AppCompatActivity;

import android.content.Intent;
import android.os.AsyncTask;
import android.os.Bundle;
import android.text.TextUtils;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.TextView;
import android.widget.Toast;

public class SettingsActivity extends AppCompatActivity {

    private TextView user;
    private EditText senha;
    private EditText repeteSenha;
    private EditText telResi;
    private EditText telComer;
    private EditText cel1;
    private EditText cel2;
    private Button enviar;
    private String baseUrl;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_settings);

        baseUrl = "http://".concat(MainActivity.ip);
        baseUrl = baseUrl.concat(":5000/usuario/" + User.getId() + "/contato");

        user = (TextView) findViewById(R.id.TV1);
        user.setText(user.getText() + User.getNome());

        try {
            ApiAuthenticationClient apiAuthenticationClient =
                    new ApiAuthenticationClient(
                            baseUrl
                            , ""
                            , ""
                            , "GET"
                    );

            AsyncTask<Void, Void, String> exec = new SettingsActivity.NetworkOperation(apiAuthenticationClient);
            exec.execute();
        } catch (Exception ex) {
        }
        enviar = (Button) findViewById(R.id.bt10);
        enviar.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                baseUrl = "http://".concat(MainActivity.ip);
                baseUrl = baseUrl.concat(":5000/usuario/" + User.getId());
                senha = (EditText) findViewById(R.id.nSenha);
                repeteSenha = (EditText) findViewById(R.id.nSenha2);
                if (senha.getText().length() == 0 || repeteSenha.getText().length() == 0) {
                    senha.setError("Os campos não podem estar em branco");
                    repeteSenha.setError("Os campos não podem estar em branco");
                }
                else if (senha.getText().toString().equals(repeteSenha.getText().toString()) == false) {
                    repeteSenha.setError("As senhas devem ser iguais");
                } else {
                    User.setSenha(repeteSenha.getText().toString());
                    User.setCelular_1(cel1.getText().toString());
                    User.setCelular_2(cel2.getText().toString());
                    User.setFone_res(telResi.getText().toString());
                    User.setFone_trab((telComer.getText().toString()));
                    try {
                        ApiAuthenticationClient apiAuthenticationClient =
                                new ApiAuthenticationClient(
                                        baseUrl
                                        , ""
                                        , ""
                                        , "PUT"
                                );

                        AsyncTask<Void, Void, String> exec = new SettingsActivity.NetworkOperation(apiAuthenticationClient);
                        exec.execute();
                    } catch (Exception ex) {
                    }
                }
            }
        });
    }

    private void goToUserActivity() {
        Intent intent = new Intent(this, UserActivity.class);
        startActivity(intent);
    }

    private void setInfo() {

        telResi = (EditText) findViewById(R.id.telResi);
        if (User.getFone_res().toString().trim().length() >= 5) {
            telResi.setText(User.getFone_res());
        }else{
            telResi.setHint("Telefone residêncial");
        }

        telComer = (EditText) findViewById(R.id.telCome);
        if (User.getFone_trab().toString().trim().length() >= 5) {
            telComer.setText(User.getFone_trab());
        }else{
            telComer.setHint("Telefone comercial");
        }

        cel1 = (EditText) findViewById(R.id.cel);
        if (User.getCelular_1().toString().trim().length() >= 5) {
            cel1.setText(User.getCelular_1());
        }else{
            cel1.setHint("Telefone celular");
        }

        cel2 = (EditText) findViewById(R.id.cel2);
        if (User.getCelular_2().toString().trim().length() >= 5) {
            cel2.setText(User.getCelular_2());
        }else{
            cel2.setHint("Telefone celular 2");
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
                isValidCredentials = apiAuthenticationClient.exec();
            } catch (Exception e) {
                e.printStackTrace();
            }

            return null;
        }


        @Override
        protected void onPostExecute(String result) {
            super.onPostExecute(result);
            if (isValidCredentials == "true") {
                setInfo();
                //Toast.makeText(getApplicationContext(), "Eventos atualizados" , Toast.LENGTH_SHORT).show();
            }
            else if (isValidCredentials == "atualizado") {
                goToUserActivity();
                Toast.makeText(getApplicationContext(), "Dados atualizados" , Toast.LENGTH_SHORT).show();
            }
        }
    }
}


