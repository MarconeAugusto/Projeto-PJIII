package pjIII.simova;

import android.util.Log;

import org.json.JSONArray;
import org.json.JSONObject;

import java.io.DataOutputStream;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.URL;
import java.util.ArrayList;
import java.util.List;
import java.util.Scanner;

/**
 * Created by user on 12/8/17.
 */

public class ApiAuthenticationClient {

    private String baseUrl;
    private String username;
    private String password;
    private String httpMethod; // GET, POST, PUT, DELETE
    private String token;
    private String nome;
    private int tipo;
    private int id;
    private List<String> vagas = new ArrayList<>();
    private List<String> eventos = new ArrayList<>();

    /**
     * @param baseUrl  String
     * @param username String
     * @param password String
     */
    public ApiAuthenticationClient(String baseUrl, String username, String password, String httpMethod) {
        this.baseUrl = baseUrl;
        this.username = username;
        this.password = password;
        this.httpMethod = httpMethod;
        // This is important. The application may break without this line.
        System.setProperty("jsse.enableSNIExtension", "false");
    }


    /**
     * Make the call to the Rest API and return its response as a string.
     *
     * @return String
     */
    public String execute() {
        try {
            StringBuilder urlString = new StringBuilder(baseUrl);

            URL url = new URL(urlString.toString());

            Log.i("URL", String.valueOf(url));

            HttpURLConnection connection = (HttpURLConnection) url.openConnection();
            connection.setRequestProperty("Accept", "application/json");
            connection.setRequestProperty("Content-type", "application/json");
            connection.setRequestMethod(httpMethod);
            connection.setConnectTimeout(5000);
            connection.setDoInput(true);
            connection.setDoOutput(true);

            JSONObject jsonParam = new JSONObject();
            jsonParam.put("email", username);
            jsonParam.put("senha", password);

            Log.i("JSON", jsonParam.toString());
            DataOutputStream os = new DataOutputStream(connection.getOutputStream());
            os.writeBytes(jsonParam.toString());

            os.flush();
            os.close();

            connection.connect();

            Log.i("STATUS", String.valueOf(connection.getResponseCode()));
            Log.i("MSG", connection.getResponseMessage());

            if (connection.getResponseCode() == 200) {
                InputStream inputStream = connection.getInputStream();
                InputStreamReader inputStreamReader = new InputStreamReader(inputStream, "UTF-8");
                Scanner scanner = new Scanner(inputStreamReader);
                StringBuffer stringBuffer = new StringBuffer();
                while (scanner.hasNext()) {
                    stringBuffer.append(scanner.nextLine());
                }
                System.out.println("STRING BUFFER >>>>>>>" +stringBuffer);
                JSONObject jsonObject = new JSONObject(stringBuffer.toString());
                JSONArray jsonArray = (JSONArray) jsonObject.get("vagas");
                nome = jsonObject.getString("nome");
                tipo = jsonObject.getInt("tipo");
                token = jsonObject.getString("token");
                id = jsonObject.getInt("id");
                if (tipo == 1) {
                    return "admin";
                }
                if (jsonArray.length() == 0) {
                    return "semVaga";
                }
                for (int j = 0; j < jsonArray.length(); j++) {
                    JSONObject jsonObject2 = (JSONObject) jsonArray.get(j);
                    System.out.println(jsonObject2);
                    vagas.add(jsonObject2.getString("identificador"));
                    vagas.add(String.valueOf(jsonObject2.getInt("estado")));
                    vagas.add(String.valueOf(jsonObject2.getInt("id")));
                }
                Log.i("NOME", String.valueOf(nome));
                Log.i("TIPO", String.valueOf(tipo));
                Log.i("TOKEN", String.valueOf(token));
                Log.i("VAGAS", String.valueOf(vagas));


                User user = new User();
                user.setNome(nome);
                user.setToken(token);
                user.setVagas(vagas);
                user.setId(id);
                return "true";
            }
            if (connection.getResponseCode() == 401 || connection.getResponseCode() == 403) {
                return "invalid";
            }
            connection.disconnect();
        } catch (Exception e) {
            e.printStackTrace();
        }
        return "false";
    }


    /**
     * Make the call to the Rest API and return its response as a string.
     *
     * @return String
     */
    public String ex() {
        try {
            //StringBuilder urlString = new StringBuilder(baseUrl);
            URL url = new URL(baseUrl);

            Log.i("URL", String.valueOf(url));
            Log.i("MÉTODO", String.valueOf(httpMethod));
            Log.i("TOKEN", String.valueOf(User.getToken()));

            HttpURLConnection connection = (HttpURLConnection) url.openConnection();
            connection.setRequestMethod(httpMethod);
            connection.setRequestProperty("Authorization", User.getToken());
            connection.setRequestProperty("Accept", "application/json");
            connection.setRequestProperty("Content-type", "application/json");
            connection.connect();

            Log.i("STATUS", String.valueOf(connection.getResponseCode()));
            Log.i("MSG", connection.getResponseMessage());

            if (connection.getResponseCode() == 200) {
                InputStream inputStream = connection.getInputStream();
                InputStreamReader inputStreamReader = new InputStreamReader(inputStream, "UTF-8");
                Scanner scanner = new Scanner(inputStreamReader);
                StringBuffer stringBuffer = new StringBuffer();
                while (scanner.hasNext()) {
                    stringBuffer.append(scanner.nextLine());
                }
                JSONObject jsonObject = new JSONObject(stringBuffer.toString());
                JSONArray jsonArray = (JSONArray) jsonObject.get("eventos");
                for (int j = 0; j < jsonArray.length(); j++) {
                    JSONObject jsonObject2 = (JSONObject) jsonArray.get(j);
                    eventos.add(jsonObject2.getString("data"));
                    eventos.add(jsonObject2.getString("tipo"));
                    eventos.add(String.valueOf(jsonObject2.getInt("tipo_int")));

                }
                User.setEventos(eventos);
                Log.i("LISTA DE EVENTOS >>>>>", String.valueOf(eventos));
                connection.disconnect();
                return "true";
            }
            if (connection.getResponseCode() == 401 || connection.getResponseCode() == 403) {
                connection.disconnect();
                return "invalid";

            }
        } catch (Exception e) {
            e.printStackTrace();
        }
        return "false";
    }

    /**
     * Make the call to the Rest API and return its response as a string.
     *
     * @return String
     */
    public String exec() {
        try {
            if (httpMethod == "GET"){
                //StringBuilder urlString = new StringBuilder(baseUrl);
                URL url = new URL(baseUrl);

                Log.i("URL", String.valueOf(url));
                Log.i("MÉTODO", String.valueOf(httpMethod));
                Log.i("TOKEN", String.valueOf(User.getToken()));

                HttpURLConnection connection = (HttpURLConnection) url.openConnection();
                connection.setRequestMethod(httpMethod);
                connection.setRequestProperty("Authorization", User.getToken());
                connection.setRequestProperty("Accept", "application/json");
                connection.setRequestProperty("Content-type", "application/json");
                connection.connect();

                Log.i("STATUS", String.valueOf(connection.getResponseCode()));
                Log.i("MSG", connection.getResponseMessage());

                if (connection.getResponseCode() == 200) {
                    InputStream inputStream = connection.getInputStream();
                    InputStreamReader inputStreamReader = new InputStreamReader(inputStream, "UTF-8");
                    Scanner scanner = new Scanner(inputStreamReader);
                    StringBuffer stringBuffer = new StringBuffer();
                    while (scanner.hasNext()) {
                        stringBuffer.append(scanner.nextLine());
                    }
                    System.out.println(stringBuffer);
                    JSONObject jsonObject = new JSONObject(stringBuffer.toString());
                    User.setCelular_1(jsonObject.getString("celular_1"));
                    User.setCelular_2(jsonObject.getString("celular_2"));
                    User.setFone_res(jsonObject.getString("fone_residencial"));
                    User.setFone_trab(jsonObject.getString("fone_trabalho"));
                    Log.i("CEL 1", User.getCelular_1());
                    Log.i("CEL 2", User.getCelular_2());
                    Log.i("FON 1", User.getFone_res());
                    Log.i("FON 2", User.getFone_trab());

                    connection.disconnect();
                    return "true";
                }
                if (connection.getResponseCode() == 401 || connection.getResponseCode() == 403) {
                    connection.disconnect();
                    return "invalid";

                }
            } if (httpMethod == "PUT"){
                URL url = new URL(baseUrl);

                Log.i("URL", String.valueOf(url));
                Log.i("MÉTODO", String.valueOf(httpMethod));
                Log.i("TOKEN", String.valueOf(User.getToken()));

                HttpURLConnection connection = (HttpURLConnection) url.openConnection();
                connection.setRequestMethod(httpMethod);
                connection.setRequestProperty("Authorization", User.getToken());
                connection.setRequestProperty("Accept", "application/json");
                connection.setRequestProperty("Content-type", "application/json");
                JSONObject jsonParam = new JSONObject();
                jsonParam.put("senha", User.getSenha());
                jsonParam.put("celular_1", User.getCelular_1());
                jsonParam.put("celular_2", User.getCelular_2());
                jsonParam.put("fone_residencial", User.getFone_res());
                jsonParam.put("fone_trabalho", User.getFone_trab());

                Log.i("JSON", jsonParam.toString());
                DataOutputStream os = new DataOutputStream(connection.getOutputStream());
                os.writeBytes(jsonParam.toString());

                os.flush();
                os.close();
                connection.connect();

                Log.i("STATUS", String.valueOf(connection.getResponseCode()));
                Log.i("MSG", connection.getResponseMessage());

                if (connection.getResponseCode() == 200) {
                    connection.disconnect();
                    return "atualizado";
                }else{
                    connection.disconnect();
                    return "false";
                }

            }
        }catch (Exception e) {
            e.printStackTrace();
        }
        return "false";
    }

}
