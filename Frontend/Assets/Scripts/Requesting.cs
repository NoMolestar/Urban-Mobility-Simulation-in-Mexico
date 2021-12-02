using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.Networking;



public class Requesting : MonoBehaviour
{
    public GameObject carrosVerticales;
    public GameObject carrosHorizontales;
    public List<GameObject> cars = new List<GameObject>();
    private bool flag = true;

    void Start()
    {
        StartCoroutine(GetText());
    }

    IEnumerator GetText()
    {
        UnityWebRequest www = UnityWebRequest.Get("http://localhost:5000/");
        yield return www.SendWebRequest();

        if (www.result != UnityWebRequest.Result.Success)
        {
            Debug.Log(www.error);
        }

        Data posiciones = JsonUtility.FromJson<Data>(www.downloadHandler.text);
        foreach (Position p in posiciones.data)
        {
            int vCarros = p.vCars;
            int hCarros = p.hCars;
            int i = 0;
            foreach (Position_Aux pAux in p.posiciones)
            {
                if (!flag)
                {    
                    cars[i].transform.position = new Vector3(pAux.valor[1], 0, pAux.valor[0]);
                }
                else
                {
                    if (pAux.direccion == 0)
                    {
                        cars.Add(Instantiate(carrosVerticales, new Vector3(pAux.valor[1], 0, pAux.valor[0]), Quaternion.identity) as GameObject);

                    }
                    else
                    {
                        cars.Add(Instantiate(carrosHorizontales, new Vector3(pAux.valor[1], 0, pAux.valor[0]), Quaternion.identity) as GameObject);
                    }
                }
                i += 1;
            }
            i = 0;
            flag = false;
        }
        yield return new WaitForSeconds(2);
        StartCoroutine(GetText());
    }
}
