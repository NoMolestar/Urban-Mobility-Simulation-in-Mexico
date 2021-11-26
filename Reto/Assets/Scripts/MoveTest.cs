using System.Collections;
using UnityEngine;
using UnityEngine.Networking;
using TMPro;

public class MoveTest : MonoBehaviour
{
    public float speed;
    public Transform[] obj;
    public Transform[] targets;

    void Start()
    {
        StartCoroutine(GetText());
    }

    void Update()
    {
        for(int i = 0; i < obj.Length; i++)
        {
            obj[i].LookAt(targets[i]);
            obj[i].position = Vector3.MoveTowards(obj[i].position,new Vector3(targets[i].position.x,obj[i].position.y,obj[i].position.z), speed*Time.deltaTime);
        }
    }

    IEnumerator GetText() {
        while(true){
            float inicio = Time.time;
            UnityWebRequest www = UnityWebRequest.Get("http://localhost:8000/");
            yield return www.SendWebRequest();
    
            if (www.result != UnityWebRequest.Result.Success) {
                Debug.LogWarning(www.error);
            }

            Data posiciones = JsonUtility.FromJson<Data>(www.downloadHandler.text);

            int i = 0;
            foreach(Position p in posiciones.data){
                obj[i].position = Vector3.MoveTowards(obj[i].position,new Vector3(p.x,p.y,p.z),2f);
                i++;
            }

            float total = Time.time - inicio;
        
            yield return new WaitForSeconds(3f);
        }
    }

}
