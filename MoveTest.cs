using System.Collections;
using UnityEngine;
using UnityEngine.Networking;
using TMPro;

public class MoveTest : MonoBehaviour
{
    public float speed;
    public Transform[] obj;
    public Transform[] targets;
    public Camera cam;
    public Vector3 offset;
    public GameObject carInfoPanel;
    public TextMeshProUGUI carInfoText;
    public TextMeshProUGUI velocityInfoText;
    public TextMeshProUGUI targetInfoText;

    private bool followingCar;
    private Transform car;
    private Vector3 defaultPos;
    private Quaternion defaultRot;

    void Start()
    {
        defaultPos = cam.transform.position;
        defaultRot = cam.transform.rotation;
        StartCoroutine(GetText());
    }

    void Update()
    {
        for(int i = 0; i < obj.Length; i++)
        {
            obj[i].LookAt(targets[i]);
            obj[i].position = Vector3.MoveTowards(obj[i].position,new Vector3(targets[i].position.x,obj[i].position.y,obj[i].position.z), speed*Time.deltaTime);
        }
    
        if(Input.GetMouseButtonDown(0))
        {
            RaycastHit hitInfo = new RaycastHit();
            bool hit = Physics.Raycast(Camera.main.ScreenPointToRay(Input.mousePosition), out hitInfo);
            if (hit) 
            {
                if (hitInfo.transform.gameObject.tag == "Car")
                {
                    car = hitInfo.transform;
                    followingCar = true;
                }
                else
                {
                    followingCar = false;
                }
            }
            else
            {
                followingCar = false;
            }
        }

        if(followingCar)
        {
            cam.transform.LookAt(car);
            cam.transform.position = car.position + offset;
            ShowCarInfo();
        }
        else
        {
            cam.transform.position = defaultPos;
            cam.transform.rotation = defaultRot;
            HideCarInfo();
        }
    
    }

    void ShowCarInfo()
    {
        carInfoPanel.SetActive(true);
        carInfoText.text = car.transform.gameObject.name;
        velocityInfoText.text = speed.ToString();
        targetInfoText.text = targets[0].position.x.ToString() + ", " + targets[0].position.y.ToString() + ", " + targets[0].position.z.ToString();
    }

    void HideCarInfo()
    {
        carInfoPanel.SetActive(false);
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
