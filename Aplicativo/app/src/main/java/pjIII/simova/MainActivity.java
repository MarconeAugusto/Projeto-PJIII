package pjIII.simova;

import androidx.appcompat.app.AppCompatActivity;

import android.app.AlertDialog;
import android.content.DialogInterface;
import android.content.Intent;
import android.os.AsyncTask;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.ProgressBar;
import android.widget.Toast;

import static android.view.View.GONE;
import static android.view.View.VISIBLE;


public class MainActivity extends AppCompatActivity {

    private Button button_login;
    private EditText email;
    private EditText senha;
    private String username;
    private String password;
    //public static String ip = "192.168.0.14";
    //public static String ip = "10.206.1.131";
    public static String ip = "ubuntu@ec2-18-218-125-147.us-east-2.compute.amazonaws.com";
    private String baseUrl;
    private ProgressBar progressBar;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        // TODO: Replace this with your own IP address or URL.
        baseUrl = "http://".concat(ip);
        baseUrl = baseUrl.concat(":5000/usuario/login");

        email = (EditText) findViewById(R.id.email);
        senha = (EditText) findViewById(R.id.senha);
        button_login = (Button) findViewById(R.id.button);
        progressBar = (ProgressBar) findViewById(R.id.progressBar);
        progressBar.setVisibility(GONE);

        button_login.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                try {

                    progressBar.setVisibility(VISIBLE);

                    username = email.getText().toString();
                    password = senha.getText().toString();

                    ApiAuthenticationClient apiAuthenticationClient =
                            new ApiAuthenticationClient(
                                    baseUrl
                                    , username
                                    , password
                                    , "POST"
                            );

                    AsyncTask<Void, Void, String> execute = new ExecuteNetworkOperation(apiAuthenticationClient);
                    execute.execute();
                } catch (Exception ex) {
                }
            }
        });
    }

    @Override
    public void onBackPressed() {
        AlertDialog.Builder builder = new AlertDialog.Builder(this, R.style.Theme_AppCompat_Light_Dialog_Alert);
        builder.setMessage("Deseja realmente sair do aplicativo?")
                .setCancelable(false)
                .setPositiveButton("Sim", new DialogInterface.OnClickListener() {
                    public void onClick(DialogInterface dialog, int id) {

                        Intent intent = new Intent(Intent.ACTION_MAIN);
                        intent.addCategory(Intent.CATEGORY_HOME);
                        intent.setFlags(Intent.FLAG_ACTIVITY_NEW_TASK);
                        startActivity(intent);
                        finish();
                    }
                })
                .setNegativeButton("Não", new DialogInterface.OnClickListener() {
                    public void onClick(DialogInterface dialog, int id) {
                        dialog.cancel();
                    }
                });
        AlertDialog alert = builder.create();
        alert.show();

    }

    /**
     * Open a new activity window.
     */
    private void goToUserActivity() {
        Intent intent = new Intent(this, UserActivity.class);
        startActivity(intent);
    }

    public class ExecuteNetworkOperation extends AsyncTask<Void, Void, String> {

        private ApiAuthenticationClient apiAuthenticationClient;
        private String isValidCredentials;

        /**
         * Overload the constructor to pass objects to this class.
         */
        public ExecuteNetworkOperation(ApiAuthenticationClient apiAuthenticationClient) {
            this.apiAuthenticationClient = apiAuthenticationClient;
        }

        @Override
        protected String doInBackground(Void... params) {
            try {
                isValidCredentials = apiAuthenticationClient.execute();
            } catch (Exception e) {
                e.printStackTrace();
            }

            return null;
        }

        @Override
        protected void onPostExecute(String result){
            super.onPostExecute(result);
            // Login Success
            if (isValidCredentials == "true"){
                progressBar.setVisibility(GONE);
                Toast.makeText(getApplicationContext(), "Bem vindo, "+ User.getNome() , Toast.LENGTH_LONG).show();
                goToUserActivity();
            } else if (isValidCredentials == "admin") {
                progressBar.setVisibility(GONE);
                Toast.makeText(getApplicationContext(), "O aplicativo não é destinado para administradores", Toast.LENGTH_LONG).show();
            } else if (isValidCredentials == "invalid") {
                progressBar.setVisibility(GONE);
                Toast.makeText(getApplicationContext(), "Login Inválido", Toast.LENGTH_LONG).show();
            } else if (isValidCredentials == "semVaga") {
                progressBar.setVisibility(GONE);
                Toast.makeText(getApplicationContext(), "Usuário não possui vagas para monitorar", Toast.LENGTH_LONG).show();
            }else {// Login Failure
                progressBar.setVisibility(GONE);
                Toast.makeText(getApplicationContext(), "Falha no login", Toast.LENGTH_LONG).show();
            }
        }
    }
}
