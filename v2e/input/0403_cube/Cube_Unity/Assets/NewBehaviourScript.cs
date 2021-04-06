using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class NewBehaviourScript : MonoBehaviour
{
   
    // Update is called once per frame
    void Update()
    {
        transform.position = new Vector3(0, 0, 0);
        
        transform.Rotate(new Vector3(0f, 150f, 0f) * Time.deltaTime);
        
//        transform.rotation = Quaternion.Euler (new Vector3 (10, 0, 0));
    }
}

