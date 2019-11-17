###############################################################################
#import generics packages
###############################################################################
import json
###############################################################################
#import "de la casa" packages
###############################################################################
import lantools
###############################################################################
#import local
###############################################################################
import motion_func

###############################################################################
#
#
#             rabbitMQ
#
#
###############################################################################
###############################################################################
#Channel declaration
###############################################################################
IP = lantools.config.IPadress()
global channel
channel = lantools.rabbit_utilities.tunel(IP['mother'])
disp_IP = True
if disp_IP is True:
    print('Server adress RabbitMQ: ' + IP['mother'])


###############################################################################
#
#
#            Worker
#
#
###############################################################################
###############################################################################
#worker declaration
###############################################################################


def motion_worker():
    """RabbitMQ  type worker. Use motion_control queue
    """

    ###############################################################################
    """Queue preparation"""
    ###############################################################################
    print('[>] Hunting the rabbits.')
    lantools.rabbit_tools.rabbit_hunter(channel, lantools.config.giveme_queue_('motion'))
    ###############################################################################
    """Worker start consumings"""
    ###############################################################################
    print("[>>>]  Starting the motion worker...")
    lantools.rabbit_utilities.active_worker_basic(channel, 'motion_control', decide_action_motion)
    print("[xxx]  Terminating the motion worker...")



#################################################
#      Respons
#################################################



def decide_action_motion(ch, method, properties, body):
    """Worker respons
    
    Args:
        ch (TYPE): rabbitMQ channels
        method (TYPE): Description
        properties (TYPE): Description
        body (Dico): contain a 'positions' key
    """
    #################################################
    #      message unpacking
    #################################################
    #load the message under try condition
    try:
        trans_cmd = body
        bodydes = json.loads(trans_cmd)
        order = bodydes['order']
    except Exception:
        print('[xxx] Error: motion call, wrong message format!')


    #################################################
    #      verbosity
    #################################################
    print('-------------------------------')
    print("New order motion is: " + order)


    #################################################
    #      ckeck order
    #################################################
    if order == 'move':
        #Debug
        debug = True
        if debug is True:
            print('Do x , DO X!')

        #Action proper
        motion_func.move_raspberry(order)
        lantools.rabbit_utilities.sender(channel, 'moved', 'motion_rpc')

    elif order == 'crash':
        ch.basic_ack(delivery_tag=method.delivery_tag)  # because of crash, acredit before
        print('[*] Motor will crash!')
        motion_func.move_raspberry('taart!')

    #################################################
    #       """UnKnonw respons"""
    #################################################
    else:
        #This is an error chuchy
        print("[???] Order is Unknown motion: " + str(order))

    ch.basic_ack(delivery_tag=method.delivery_tag)  # give validation consumption





