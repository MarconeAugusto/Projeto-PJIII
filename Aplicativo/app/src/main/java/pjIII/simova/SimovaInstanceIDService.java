package pjIII.simova;

import android.util.Log;

import com.google.firebase.iid.FirebaseInstanceId;
import com.google.firebase.iid.FirebaseInstanceIdService;

public class SimovaInstanceIDService extends FirebaseInstanceIdService {
    public String token;

    @Override
    public void onTokenRefresh(){
        super.onTokenRefresh();

        token = FirebaseInstanceId.getInstance().getToken();
        Log.d("Token da APP" ,token);
    }
}
