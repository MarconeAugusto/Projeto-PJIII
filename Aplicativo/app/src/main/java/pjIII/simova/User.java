package pjIII.simova;

import java.util.List;

public class User {


    private static String Nome;
    private static String token;
    public static List<String> vagas;
    public static List<String> eventos;
    private static String celular_1;
    private static String celular_2;
    private static String fone_res;
    private static String fone_trab;
    private static String senha;
    private static int id;


    public static String getSenha() {
        return senha;
    }

    public static void setSenha(String senha) {
        User.senha = senha;
    }

    public static String getCelular_1() {
        return celular_1;
    }

    public static void setCelular_1(String celular_1) {
        User.celular_1 = celular_1;
    }

    public static String getCelular_2() {
        return celular_2;
    }

    public static void setCelular_2(String celular_2) {
        User.celular_2 = celular_2;
    }

    public static String getFone_res() {
        return fone_res;
    }

    public static void setFone_res(String fone_res) {
        User.fone_res = fone_res;
    }

    public static String getFone_trab() {
        return fone_trab;
    }

    public static void setFone_trab(String fone_trab) {
        User.fone_trab = fone_trab;
    }

    public static int getId() {
        return id;
    }

    public static void setId(int id) {
        User.id = id;
    }

    public static String getEventos(int pos) {
        if (eventos.get(pos)!= null){
            return eventos.get(pos);
        }else
            return null;
    }

    public static void setEventos(List<String> eventos) {
        User.eventos = eventos;
    }

    public static String getNome() {
        return Nome;
    }

    public void setNome(String nome) {
        Nome = nome;
    }

    public static String getToken() {
        return token;
    }

    public void setToken(String token) {
        this.token = token;
    }

    public List<String> getVagas() {
        return vagas;
    }

    public static String getVaga(int pos){
        return vagas.get(pos);
    }

    public void setVagas(List<String> vagas) {
        this.vagas = vagas;
    }
}
